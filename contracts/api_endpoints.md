# NEXUS — API Endpoints Contract
### SIH 2026 · REST API Specification (FastAPI Backend, Owned by P1, Consumed by P4)

Base URL: `http://localhost:8000/api/v1`

---

## 1. Ingestion Endpoints

### `POST /ingest/fir`
Upload and process one or more FIR documents.
- **Request**: Multipart Form Data (`files: List[UploadFile]`, `case_id: str`)
- **Response**:
  ```json
  {
    "status": "success",
    "case_id": "sandstorm",
    "files_processed": 4,
    "entities_extracted": 42,
    "relationships_created": 38
  }
  ```

### `POST /ingest/cdr`
Upload and ingest CDR CSV file.
- **Request**: Multipart Form Data (`file: UploadFile`, `case_id: str`)
- **Response**:
  ```json
  {
    "status": "success",
    "case_id": "sandstorm",
    "records_ingested": 3033,
    "unique_numbers": 284,
    "call_edges_upserted": 412
  }
  ```

### `POST /ingest/transactions`
Upload and ingest banking/hawala transaction CSV.
- **Request**: Multipart Form Data (`file: UploadFile`, `case_id: str`)
- **Response**:
  ```json
  {
    "status": "success",
    "case_id": "sandstorm",
    "transactions_ingested": 600,
    "transacted_edges_upserted": 210
  }
  ```

---

## 2. Graph & Analytics Endpoints

### `GET /graph/{case_id}`
Returns the complete or filtered graph in Cytoscape.js JSON format.
- **Query Params**: `min_confidence` (float, default 0.5), `include_noise` (bool, default false)
- **Response**:
  ```json
  {
    "nodes": [
      {
        "data": {
          "id": "P001",
          "label": "Arjun Mehta",
          "type": "Person",
          "is_suspect": true,
          "role": "Ring leader",
          "pagerank_score": 0.284,
          "betweenness_score": 0.412,
          "community_id": 1,
          "aliases": ["A. Mehta", "Arjun Mehata"],
          "source_docs": ["fir_sandstorm_1.txt", "fir_sandstorm_2.txt"]
        }
      }
    ],
    "edges": [
      {
        "data": {
          "id": "e_P001_P002",
          "source": "P001",
          "target": "P002",
          "label": "CALLED",
          "weight": 14.0,
          "confidence": 0.95,
          "details": "14 calls in 48h pre-incident"
        }
      }
    ]
  }
  ```

### `GET /alerts/{case_id}`
Returns all detected anomalies categorized across the 4 detection layers.
- **Response**:
  ```json
  {
    "case_id": "sandstorm",
    "total_alerts": 3,
    "alerts": [
      {
        "alert_id": "ANO-001",
        "severity": "CRITICAL",
        "layer": "Statistical + Rule (Layer 1 & 2)",
        "title": "Burst Coordination Pattern",
        "description": "Phone +91-98400-11111 (Arjun Mehta) placed 14 calls in 48h before seizure (Z-score: 3.82)",
        "involved_entities": ["P001", "P002", "P003"],
        "timestamp": "2025-03-14T23:50:00"
      },
      {
        "alert_id": "ANO-002",
        "severity": "HIGH",
        "layer": "Unsupervised ML (Layer 3 IsolationForest)",
        "title": "Suspected Structuring (Smurfing)",
        "description": "10 consecutive transactions between ₹9.80L and ₹9.95L just below ₹10L reporting threshold",
        "involved_entities": ["ACC001", "ACC002"],
        "timestamp": "2025-03-13T16:00:00"
      }
    ]
  }
  ```

---

## 3. Human-in-the-Loop Review Queue

### `GET /review-queue`
Returns low-confidence entity merge candidates awaiting supervisor approval.
- **Response**:
  ```json
  {
    "pending_count": 2,
    "items": [
      {
        "merge_id": "merge_001",
        "entity_1": {"name": "Arjun Mehata", "doc": "fir_sandstorm_2.txt", "phone": "+91-98400-11111"},
        "entity_2": {"name": "A. Mehta", "doc": "fir_sandstorm_1.txt", "phone": "+91-98400-11111"},
        "similarity_score": 0.89,
        "match_reason": "Exact phone match (+91-98400-11111) + High Jaro-Winkler name similarity (0.89)"
      }
    ]
  }
  ```

### `POST /review-queue/{merge_id}/action`
Approve or reject candidate merge.
- **Request Body**: `{"action": "APPROVE" | "REJECT", "investigator_notes": "string"}`
- **Response**: `{"status": "merged", "canonical_id": "P001", "audit_logged": true}`

---

## 4. Query & Agentic Brief Generation

### `POST /query`
Natural language query console driven by the LangGraph Orchestrator & Analyst Agent.
- **Request Body**:
  ```json
  {
    "case_id": "sandstorm",
    "query": "Find the hidden connection between Arjun Mehta and Phoenix Exports and summarize evidence"
  }
  ```
- **Response**:
  ```json
  {
    "query": "Find the hidden connection between Arjun Mehta and Phoenix Exports...",
    "plan_executed": ["find_shortest_path", "get_financial_transactions", "generate_brief"],
    "summary": "Arjun Mehta (P001) controls Phoenix Exports Pvt Ltd (ORG001) via direct bank account transfers and shell company ownership.",
    "key_findings": [
      {
        "finding": "10 structured transactions totaling ₹98.7L routed from ACC001 to ACC002.",
        "cited_nodes": ["P001", "ORG001", "ACC001", "ACC002"],
        "evidence_sources": ["fir_sandstorm_3.txt", "txn_sandstorm.csv"]
      }
    ],
    "highlighted_subgraph": {
      "node_ids": ["P001", "ACC001", "ACC002", "ORG001"],
      "edge_ids": ["e_P001_ACC001", "e_ACC001_ACC002", "e_ACC002_ORG001"]
    },
    "confidence_score": 0.94
  }
  ```

---

## 5. Audit Log

### `GET /audit-log`
Append-only log of every query, merge, and analysis decision.
- **Response**:
  ```json
  {
    "logs": [
      {
        "timestamp": "2026-09-01T15:30:00Z",
        "user": "Lead Investigator",
        "action": "APPROVED_ENTITY_MERGE",
        "details": "Merged 'Arjun Mehata' into 'Arjun Mehta' (P001)",
        "ip": "127.0.0.1"
      }
    ]
  }
  ```
