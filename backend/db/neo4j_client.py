"""
neo4j_client.py
Neo4j Database Client with connection pooling, Cypher query helpers,
active self-healing reconnection, and resilient In-Memory Graph BFS fallback.
"""

import os
import time
from typing import List, Dict, Any, Optional
from collections import deque

try:
    from neo4j import GraphDatabase
    HAS_NEO4J_DRIVER = True
except ImportError:
    HAS_NEO4J_DRIVER = False


class Neo4jClient:
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "nexus1234")
        self.driver = None
        self.is_connected = False
        self._last_reconnect_attempt = 0.0
        self._reconnect_cooldown = 5.0  # Attempt reconnect at most every 5 seconds
        
        # In-memory graph storage fallback (preserves state even when offline)
        self.in_memory_nodes: Dict[str, Dict[str, Any]] = {}
        self.in_memory_edges: List[Dict[str, Any]] = []

        self._try_connect()

    def _try_connect(self) -> bool:
        """Attempt to establish a connection to Neo4j."""
        if not HAS_NEO4J_DRIVER:
            print("[Neo4jClient] neo4j package not installed. Operating in in-memory graph mode.")
            self.is_connected = False
            return False

        try:
            if self.driver:
                try:
                    self.driver.close()
                except Exception:
                    pass
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            with self.driver.session() as session:
                session.run("RETURN 1")
            
            was_offline = not self.is_connected
            self.is_connected = True
            print(f"[Neo4jClient] Connected successfully to Neo4j at {self.uri}")

            # If we were previously offline and accumulated in-memory data, sync it now!
            if was_offline and (self.in_memory_nodes or self.in_memory_edges):
                print(f"[Neo4jClient] Network restored: Synchronizing {len(self.in_memory_nodes)} in-memory nodes to Neo4j...")
                self._sync_in_memory_to_neo4j()

            return True
        except Exception as e:
            self.is_connected = False
            self.driver = None
            return False

    def ensure_connection(self) -> bool:
        """
        Active self-healing check:
        If not currently connected, attempts to reconnect if the cooldown has elapsed.
        Switches seamlessly back to Neo4j as soon as Docker/network is restored.
        """
        if self.is_connected and self.driver:
            return True

        now = time.time()
        if now - self._last_reconnect_attempt > self._reconnect_cooldown:
            self._last_reconnect_attempt = now
            return self._try_connect()

        return False

    def _sync_in_memory_to_neo4j(self):
        """Flushes in-memory accumulated nodes and edges into Neo4j upon reconnection."""
        if not self.is_connected or not self.driver:
            return
        try:
            with self.driver.session() as session:
                for nid, props in self.in_memory_nodes.items():
                    label = props.get("type", "Entity")
                    clean_props = {k: v for k, v in props.items() if v is not None}
                    cypher = f"MERGE (n:{label} {{id: $id}}) SET n += $props"
                    session.run(cypher, {"id": nid, "props": clean_props})

                for edge in self.in_memory_edges:
                    rel_type = edge.get("label", "CONNECTED")
                    clean_props = {k: v for k, v in edge.items() if k not in ("id", "source", "target", "label") and v is not None}
                    cypher = f"""
                    MATCH (a {{id: $source}})
                    MATCH (b {{id: $target}})
                    MERGE (a)-[r:{rel_type}]->(b)
                    SET r += $props
                    """
                    session.run(cypher, {"source": edge["source"], "target": edge["target"], "props": clean_props})
            print("[Neo4jClient] Re-sync complete. In-memory data successfully persisted to Neo4j.")
        except Exception as e:
            print(f"[Neo4jClient] Warning during re-sync to Neo4j: {e}")

    def close(self):
        if self.driver:
            try:
                self.driver.close()
            except Exception:
                pass

    def run_query(self, query: str, params: dict = None) -> List[Dict[str, Any]]:
        """Run Cypher query on Neo4j if connected."""
        self.ensure_connection()
        if not self.is_connected or not self.driver:
            return []
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except Exception as e:
            print(f"[Neo4jClient] Query error: {e}")
            self.is_connected = False
            return []

    def upsert_node(self, node_id: str, label: str, properties: dict):
        """Upsert a node into both in-memory store and Neo4j (when online)."""
        props = properties.copy()
        props["id"] = node_id
        props["label"] = props.get("name", node_id)
        props["type"] = label

        self.in_memory_nodes[node_id] = props

        if self.ensure_connection():
            clean_props = {k: v for k, v in props.items() if v is not None}
            cypher = f"""
            MERGE (n:{label} {{id: $id}})
            SET n += $props
            """
            self.run_query(cypher, {"id": node_id, "props": clean_props})

    def upsert_edge(self, source_id: str, target_id: str, rel_type: str, properties: dict):
        """Upsert an edge between two nodes in both in-memory store and Neo4j (when online)."""
        edge_data = {
            "id": f"e_{source_id}_{target_id}_{rel_type}",
            "source": source_id,
            "target": target_id,
            "label": rel_type,
            **properties
        }
        # Update in-memory
        self.in_memory_edges = [e for e in self.in_memory_edges if e["id"] != edge_data["id"]]
        self.in_memory_edges.append(edge_data)

        if self.ensure_connection():
            clean_props = {k: v for k, v in properties.items() if v is not None}
            cypher = f"""
            MATCH (a {{id: $source_id}})
            MATCH (b {{id: $target_id}})
            MERGE (a)-[r:{rel_type}]->(b)
            SET r += $props
            """
            self.run_query(cypher, {"source_id": source_id, "target_id": target_id, "props": clean_props})

    def get_full_graph(self, case_id: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """Return full graph for Cytoscape.js visualization."""
        if self.ensure_connection():
            query = """
            MATCH (n)
            OPTIONAL MATCH (n)-[r]->(m)
            RETURN collect(DISTINCT n) as nodes, collect(DISTINCT {id: id(r), source: n.id, target: m.id, label: type(r), properties: properties(r)}) as edges
            """
            res = self.run_query(query)
            if res and res[0]["nodes"]:
                nodes = [{"data": dict(n)} for n in res[0]["nodes"] if n.get("id")]
                edges = [{"data": dict(e)} for e in res[0]["edges"] if e.get("source") and e.get("target")]
                return {"nodes": nodes, "edges": edges}

        # Resilient fallback to in-memory store
        nodes = [{"data": v} for v in self.in_memory_nodes.values()]
        edges = [{"data": e} for e in self.in_memory_edges]
        return {"nodes": nodes, "edges": edges}

    def shortest_path(self, source_name_or_id: str, target_name_or_id: str) -> Dict[str, Any]:
        """
        Find shortest path between two entities.
        Uses native Cypher shortestPath when Neo4j is online;
        Falls back to in-memory Breadth-First Search (BFS) when offline.
        """
        if self.ensure_connection():
            query = """
            MATCH (a), (b)
            WHERE (a.id = $src OR a.name = $src) AND (b.id = $dst OR b.name = $dst)
            MATCH p = shortestPath((a)-[*..8]-(b))
            RETURN [n in nodes(p) | {id: n.id, name: n.name, type: labels(n)[0]}] as path_nodes,
                   [r in relationships(p) | {type: type(r), source: startNode(r).id, target: endNode(r).id}] as path_edges
            """
            res = self.run_query(query, {"src": source_name_or_id, "dst": target_name_or_id})
            if res and res[0].get("path_nodes"):
                return res[0]

        # ── High-Performance In-Memory BFS Fallback ─────────────────────────
        src_id = None
        dst_id = None
        s_lower = source_name_or_id.lower().strip()
        t_lower = target_name_or_id.lower().strip()

        # Build adjacency graph first
        adj: Dict[str, List[str]] = {}
        edge_lookup: Dict[tuple, Dict[str, Any]] = {}
        for edge in self.in_memory_edges:
            u, v = str(edge["source"]), str(edge["target"])
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
            edge_lookup[(u, v)] = edge
            edge_lookup[(v, u)] = edge

        # Resolve entity IDs from ID, name, label, aliases, or edge keys
        for nid, props in self.in_memory_nodes.items():
            name = str(props.get("name", "")).lower()
            label = str(props.get("label", "")).lower()
            aliases = [str(a).lower() for a in props.get("aliases", [])]

            if not src_id:
                if nid.lower() == s_lower or name == s_lower or label == s_lower or s_lower in name or any(s_lower in a for a in aliases):
                    src_id = nid
                elif len(s_lower) > 3 and (s_lower in nid.lower() or any(a in s_lower for a in aliases)):
                    src_id = nid

            if not dst_id:
                if nid.lower() == t_lower or name == t_lower or label == t_lower or t_lower in name or any(t_lower in a for a in aliases):
                    dst_id = nid
                elif len(t_lower) > 3 and (t_lower in nid.lower() or any(a in t_lower for a in aliases)):
                    dst_id = nid

        # Fallback to direct edge endpoint IDs (e.g. phone MSISDNs, bank accounts)
        if not src_id:
            for k in adj.keys():
                if k.lower() == s_lower or s_lower in k.lower():
                    src_id = k
                    break
        if not dst_id:
            for k in adj.keys():
                if k.lower() == t_lower or t_lower in k.lower():
                    dst_id = k
                    break

        if not src_id or not dst_id:
            return {"path_nodes": [], "path_edges": []}

        if src_id == dst_id:
            props = self.in_memory_nodes.get(src_id, {})
            return {
                "path_nodes": [{"id": src_id, "name": props.get("name", src_id), "type": props.get("type", "Entity")}],
                "path_edges": []
            }

        # BFS queue stores (current_node, [path_of_nodes])
        queue = deque([(src_id, [src_id])])
        visited = {src_id}

        while queue:
            curr, path = queue.popleft()
            if curr == dst_id:
                path_nodes = []
                for node_id in path:
                    node_props = self.in_memory_nodes.get(node_id, {})
                    etype = node_props.get("type")
                    if not etype:
                        if str(node_id).startswith("+91"):
                            etype = "Phone"
                        elif "-XXXX-" in str(node_id):
                            etype = "BankAccount"
                        elif str(node_id).startswith("acc_"):
                            etype = "Person"
                        else:
                            etype = "Entity"
                    path_nodes.append({
                        "id": node_id,
                        "name": node_props.get("name", node_id),
                        "type": etype
                    })
                
                path_edges = []
                for i in range(len(path) - 1):
                    e = edge_lookup.get((path[i], path[i+1]), {})
                    path_edges.append({
                        "type": e.get("label", "CONNECTED"),
                        "source": path[i],
                        "target": path[i+1]
                    })
                return {"path_nodes": path_nodes, "path_edges": path_edges}

            for neighbor in adj.get(curr, []):
                if neighbor not in visited and len(path) < 8:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return {"path_nodes": [], "path_edges": []}


# Global singleton instance
db_client = Neo4jClient()
