"""
main.py
NEXUS Backend — FastAPI Application
Connects Agent 1 (Extractor), Agent 2 (Graph Builder), Agent 3 (Analyst),
and Supervisor Orchestrator with the Cytoscape.js Frontend.
"""

import os
import csv
import glob
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db.neo4j_client import db_client
from schemas.canonical import QueryRequest, QueryResponse, CytoscapeGraph
from agents.extractor import ExtractorAgent
from agents.graph_builder import (
    ingest_batch_to_agent2,
    load_and_run_case,
    router as agent2_router,
    init_db as init_review_db,
    get_pending_candidates,
    get_candidate,
    apply_review_decision,
    ReviewDecision,
)
from agents.analyst import analyst_agent
from agents.supervisor import supervisor_agent

app = FastAPI(
    title="NEXUS Criminal Network Analysis API",
    version="2.0.0",
    description="Agentic AI Knowledge Graph System for Law Enforcement Agencies (SIH 2026)"
)

# CORS configuration for Frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Agent 2's dedicated API router
app.include_router(agent2_router, prefix="/api/v1", tags=["Agent 2"])

# In-memory append-only audit log
audit_logs = [
    {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": "System",
        "action": "SYSTEM_STARTUP",
        "details": "NEXUS v2 Backend Initialized successfully.",
        "ip": "127.0.0.1"
    }
]

# Initialize SQLite review queue on startup
@app.on_event("startup")
def startup_init():
    init_review_db()


from fastapi.responses import FileResponse

@app.get("/")
def root():
    index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "online",
        "system": "NEXUS Criminal Network Analysis v2.0",
        "neo4j_connected": db_client.is_connected,
        "docs_url": "/docs"
    }

@app.get("/api/v1/health")
def health():
    return {
        "status": "healthy",
        "system": "NEXUS v2.0",
        "neo4j_connected": db_client.is_connected,
        "nodes_loaded": len(db_client.in_memory_nodes)
    }


# ── 1. Ingestion Endpoints ──────────────────────────────────────────────────

@app.post("/api/v1/ingest/fir")
async def ingest_fir(files: List[UploadFile] = File(...), case_id: str = Form(...)):
    """Upload and extract entities from one or more FIR documents via Supervisor Orchestrator."""
    total_entities = 0
    total_relations = 0
    all_plans = []

    for file in files:
        content = await file.read()
        res = supervisor_agent.supervise_ingestion(
            source_type="fir",
            data=content,
            case_id=case_id,
            filename=file.filename
        )
        total_entities += res.get("entities_extracted", 0)
        total_relations += res.get("relationships_created", 0)
        all_plans.extend(res.get("plan_executed", []))

    audit_logs.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": "Investigator (Badge #4401)",
        "action": "SUPERVISED_INGEST_FIR_BATCH",
        "details": f"Supervised ingestion of {len(files)} FIR files for case '{case_id}' ({total_entities} entities).",
        "ip": "127.0.0.1"
    })

    return {
        "status": "success",
        "case_id": case_id,
        "files_processed": len(files),
        "entities_extracted": total_entities,
        "relationships_created": total_relations,
        "orchestration_plan": all_plans,
    }


@app.post("/api/v1/ingest/cdr")
async def ingest_cdr(file: UploadFile = File(...), case_id: str = Form(...)):
    """Upload and ingest CDR CSV file via Supervisor Orchestrator."""
    content = await file.read()
    lines = content.decode("utf-8", errors="ignore").splitlines()
    reader = csv.DictReader(lines)
    rows = list(reader)

    res = supervisor_agent.supervise_ingestion(
        source_type="cdr",
        data=rows,
        case_id=case_id,
        filename=file.filename
    )

    audit_logs.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": "Investigator (Badge #4401)",
        "action": "SUPERVISED_INGEST_CDR_CSV",
        "details": f"Supervised ingestion of CDR file '{file.filename}' ({len(rows)} records) for case '{case_id}'.",
        "ip": "127.0.0.1"
    })

    return {
        "status": "success",
        "case_id": case_id,
        "records_ingested": len(rows),
        "entities_extracted": res.get("entities_extracted", 0),
        "relationships_created": res.get("relationships_created", 0),
        "orchestration_plan": res.get("plan_executed", []),
    }


@app.post("/api/v1/ingest/transactions")
async def ingest_transactions(file: UploadFile = File(...), case_id: str = Form(...)):
    """Upload and ingest transaction CSV file via Supervisor Orchestrator."""
    content = await file.read()
    lines = content.decode("utf-8", errors="ignore").splitlines()
    reader = csv.DictReader(lines)
    rows = list(reader)

    res = supervisor_agent.supervise_ingestion(
        source_type="txn",
        data=rows,
        case_id=case_id,
        filename=file.filename
    )

    audit_logs.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": "Investigator (Badge #4401)",
        "action": "SUPERVISED_INGEST_TXN_CSV",
        "details": f"Supervised ingestion of Transaction file '{file.filename}' ({len(rows)} records) for case '{case_id}'.",
        "ip": "127.0.0.1"
    })

    return {
        "status": "success",
        "case_id": case_id,
        "transactions_ingested": len(rows),
        "entities_extracted": res.get("entities_extracted", 0),
        "relationships_created": res.get("relationships_created", 0),
        "orchestration_plan": res.get("plan_executed", []),
    }


@app.post("/api/v1/seed/{case_id}")
def seed_case_data(case_id: str):
    """Seed the database with pre-generated case files using Agent 2's full pipeline."""
    result = load_and_run_case(case_id=case_id, sync_to_neo4j=True)
    
    # Also populate in-memory graph for the backend-level db_client (used by Agent 3)
    _sync_resolved_to_inmemory(result, bundle=result.get("_bundle"))

    return {
        "status": "seeded",
        "case_id": case_id,
        "total_input_entities": result.get("total_input_entities", 0),
        "total_resolved_entities": result.get("total_resolved_entities", 0),
        "auto_merged": result.get("auto_merged_count", 0),
        "pending_reviews": result.get("human_queue_count", 0),
        "neo4j_status": result.get("neo4j_status", "unknown"),
        "nodes_in_memory": len(db_client.in_memory_nodes),
    }


def _sync_resolved_to_inmemory(result: dict, bundle=None):
    """
    Populate the backend-level in-memory graph (db_client) from Agent 2's
    resolved entities and bundle records. This keeps Agent 3 and the graph
    visualization working even when Neo4j is offline.
    """
    # 1. Map raw entity_ids and aliases to canonical node IDs
    raw_to_canon = {}
    name_to_canon = {}
    for entity in result.get("resolved_entities", []):
        if isinstance(entity, dict):
            node_id = entity.get("canonical_id", "")
            label = entity.get("entity_type", "Unknown")
            name = entity.get("canonical_name", node_id)
            for m_id in entity.get("merged_from", []):
                raw_to_canon[m_id] = node_id
            name_to_canon[name.lower()] = node_id
            for alias in entity.get("aliases", []):
                name_to_canon[alias.lower()] = node_id

            db_client.upsert_node(
                node_id=node_id,
                label=label,
                properties={
                    "name": name,
                    "aliases": entity.get("aliases", []),
                    "confidence": entity.get("confidence", 0),
                    "sources": entity.get("sources", []),
                    "role": entity.get("role"),
                    "case_name": entity.get("case_name"),
                }
            )

    # 2. Add edges into db_client if bundle was loaded
    if bundle:
        from itertools import combinations
        # CDR edges
        for cdr in getattr(bundle, "cdr_records", []):
            db_client.upsert_edge(
                source_id=cdr.caller_msisdn,
                target_id=cdr.callee_msisdn,
                rel_type="CALLED",
                properties={"duration_sec": cdr.duration_sec, "timestamp": cdr.start_timestamp}
            )
        # Transaction edges
        for txn in getattr(bundle, "txn_records", []):
            s_id = name_to_canon.get(txn.sender_name.lower(), txn.sender_account)
            r_id = name_to_canon.get(txn.receiver_name.lower(), txn.receiver_account)
            db_client.upsert_edge(
                source_id=s_id,
                target_id=r_id,
                rel_type="TRANSACTED_WITH",
                properties={"amount_inr": txn.amount_inr, "timestamp": txn.timestamp}
            )
        # Accused co-occurrence edges
        fir_accused = {}
        for ent in getattr(bundle, "entities", []):
            if ent.type.value == "PERSON" and ent.metadata.get("role") == "accused":
                cid = raw_to_canon.get(ent.entity_id, ent.value)
                fir_accused.setdefault(ent.source_doc, []).append(cid)
        for fir_doc, accused_list in fir_accused.items():
            for a, b in combinations(set(accused_list), 2):
                db_client.upsert_edge(
                    source_id=a,
                    target_id=b,
                    rel_type="CO_ACCUSED",
                    properties={"source_doc": fir_doc}
                )


# ── 2. Graph & Analytics ─────────────────────────────────────────────────────

@app.get("/api/v1/graph/{case_id}")
def get_graph(case_id: str):
    """Get the Cytoscape graph for visual rendering."""
    # If empty, seed automatically for a smooth first-time load
    if not db_client.in_memory_nodes:
        seed_case_data(case_id)
    return db_client.get_full_graph(case_id)


@app.get("/api/v1/alerts/{case_id}")
def get_alerts(case_id: str):
    """Get multi-layer anomaly alerts."""
    alerts = analyst_agent.detect_anomalies(case_id)
    return {
        "case_id": case_id,
        "total_alerts": len(alerts),
        "alerts": alerts
    }


@app.get("/api/v1/influencers/{case_id}")
def get_influencers(case_id: str):
    """Get multi-metric influencer rankings and inferred operational roles."""
    influencers = analyst_agent.rank_key_influencers(case_id)
    return {
        "case_id": case_id,
        "total_influencers": len(influencers),
        "influencers": influencers
    }


# ── 3. Human-in-the-loop Review Queue ───────────────────────────────────────

@app.get("/api/v1/review-queue")
def get_review_queue():
    """Get candidate entity merges awaiting human approval."""
    # Pull from the real SQLite review queue
    pending = get_pending_candidates()

    # If no real candidates exist yet, provide representative demo items
    if not pending:
        from schemas.canonical import ReviewQueueItem
        demo_items = [
            ReviewQueueItem(
                merge_id="merge_001",
                entity_1={"name": "Arjun Mehata", "doc": "fir_sandstorm_2.txt", "phone": "+91-98400-11111"},
                entity_2={"name": "A. Mehta", "doc": "fir_sandstorm_1.txt", "phone": "+91-98400-11111"},
                similarity_score=0.89,
                match_reason="Exact phone match (+91-98400-11111) + High Jaro-Winkler name similarity (0.89)",
                status="PENDING"
            ),
            ReviewQueueItem(
                merge_id="merge_002",
                entity_1={"name": "Kabeer Sheikh", "doc": "fir_sandstorm_1.txt", "phone": "+91-98400-55555"},
                entity_2={"name": "K. Sheikh", "doc": "fir_sandstorm_4.txt", "phone": "+91-98400-55555"},
                similarity_score=0.84,
                match_reason="Phonetic Soundex match ('K262') + Same Address area (Dharavi)",
                status="PENDING"
            )
        ]
        items = [item.model_dump() if hasattr(item, "model_dump") else item.dict() for item in demo_items]
        return {"pending_count": len(items), "items": items}

    # Format real candidates for the frontend
    items = []
    for row in pending:
        items.append({
            "merge_id": row.get("pair_id", ""),
            "entity_1": {"name": row.get("entity_a_value", ""), "doc": row.get("entity_a_source", "")},
            "entity_2": {"name": row.get("entity_b_value", ""), "doc": row.get("entity_b_source", "")},
            "similarity_score": row.get("score", 0),
            "match_reason": row.get("signals", ""),
            "status": row.get("status", "PENDING").upper(),
        })

    return {"pending_count": len(items), "items": items}


@app.post("/api/v1/review-queue/{merge_id}/action")
def review_action(merge_id: str, action: str = Form(...), notes: str = Form(None)):
    """Approve or reject a candidate merge with audit logging."""
    # Try the real SQLite queue first
    candidate = get_candidate(merge_id)
    if candidate:
        decision = ReviewDecision(
            action="approve" if action.upper() == "APPROVED" else "reject",
            reviewer_id="Lead Investigator (Badge #4401)",
            note=notes,
        )
        success = apply_review_decision(merge_id, decision)
        if not success:
            raise HTTPException(status_code=400, detail="Merge item not pending or not found")
    
    audit_logs.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": "Lead Investigator (Badge #4401)",
        "action": f"{action.upper()}_ENTITY_MERGE",
        "details": f"Action {action.upper()} on merge candidate {merge_id}. Notes: {notes or 'None'}",
        "ip": "127.0.0.1"
    })
    return {"status": "success", "merge_id": merge_id, "action": action.upper()}


# ── 4. Natural Language Query & Brief Console ───────────────────────────────

@app.post("/api/v1/query", response_model=QueryResponse)
def execute_query(req: QueryRequest):
    """Execute natural language query through the Supervisor Agent."""
    audit_logs.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": "Investigator (Badge #4401)",
        "action": "INVESTIGATOR_NL_QUERY",
        "details": f"Query on case '{req.case_id}': \"{req.query}\"",
        "ip": "127.0.0.1"
    })
    return supervisor_agent.process_query(req)


# ── 5. Audit Log ────────────────────────────────────────────────────────────

@app.get("/api/v1/audit-log")
def get_audit_log():
    """Retrieve immutable audit logs."""
    return {"total_events": len(audit_logs), "logs": list(reversed(audit_logs))}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
