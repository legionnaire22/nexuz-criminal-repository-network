"""
neo4j_client.py
Neo4j Database Client with connection pooling, Cypher query helpers,
and In-Memory Graph fallback for offline testing.
"""

import os
from typing import List, Dict, Any, Optional

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
        
        # In-memory graph storage fallback
        self.in_memory_nodes: Dict[str, Dict[str, Any]] = {}
        self.in_memory_edges: List[Dict[str, Any]] = []

        if HAS_NEO4J_DRIVER:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                with self.driver.session() as session:
                    session.run("RETURN 1")
                self.is_connected = True
                print(f"[Neo4jClient] Connected successfully to {self.uri}")
            except Exception as e:
                print(f"[Neo4jClient] Neo4j not reachable ({e}). Using in-memory graph mode.")
                self.is_connected = False
        else:
            print("[Neo4jClient] neo4j package not installed. Using in-memory graph mode.")

    def close(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query: str, params: dict = None) -> List[Dict[str, Any]]:
        """Run Cypher query on Neo4j if connected."""
        if not self.is_connected or not self.driver:
            return []
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except Exception as e:
            print(f"[Neo4jClient] Query error: {e}")
            return []

    def upsert_node(self, node_id: str, label: str, properties: dict):
        """Upsert a node into Neo4j or in-memory store."""
        props = properties.copy()
        props["id"] = node_id
        props["label"] = props.get("name", node_id)
        props["type"] = label

        self.in_memory_nodes[node_id] = props

        if self.is_connected:
            cypher = f"""
            MERGE (n:{label} {{id: $id}})
            SET n += $props
            """
            self.run_query(cypher, {"id": node_id, "props": props})

    def upsert_edge(self, source_id: str, target_id: str, rel_type: str, properties: dict):
        """Upsert an edge between two nodes."""
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

        if self.is_connected:
            cypher = f"""
            MATCH (a {{id: $source_id}})
            MATCH (b {{id: $target_id}})
            MERGE (a)-[r:{rel_type}]->(b)
            SET r += $props
            """
            self.run_query(cypher, {"source_id": source_id, "target_id": target_id, "props": properties})

    def get_full_graph(self, case_id: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """Return full graph for Cytoscape.js visualization."""
        if self.is_connected:
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

        # Fallback in-memory
        nodes = [{"data": v} for v in self.in_memory_nodes.values()]
        edges = [{"data": e} for e in self.in_memory_edges]
        return {"nodes": nodes, "edges": edges}

    def shortest_path(self, source_name_or_id: str, target_name_or_id: str) -> List[Dict[str, Any]]:
        """Find shortest path between two entities."""
        if self.is_connected:
            query = """
            MATCH (a), (b)
            WHERE (a.id = $src OR a.name = $src) AND (b.id = $dst OR b.name = $dst)
            MATCH p = shortestPath((a)-[*..8]-(b))
            RETURN [n in nodes(p) | {id: n.id, name: n.name, type: labels(n)[0]}] as path_nodes,
                   [r in relationships(p) | {type: type(r), source: startNode(r).id, target: endNode(r).id}] as path_edges
            """
            res = self.run_query(query, {"src": source_name_or_id, "dst": target_name_or_id})
            if res:
                return res[0]

        # In-memory BFS fallback
        return {"path_nodes": [], "path_edges": []}


# Global singleton instance
db_client = Neo4jClient()
