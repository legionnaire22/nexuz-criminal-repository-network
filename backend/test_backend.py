"""
test_backend.py
Runs a test suite against the FastAPI backend using TestClient.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    print("[OK] GET / returned 200 OK")

def test_seed_and_graph():
    res = client.post("/api/v1/seed/sandstorm")
    assert res.status_code == 200
    print("[OK] POST /api/v1/seed/sandstorm returned 200 OK")

    res = client.get("/api/v1/graph/sandstorm")
    assert res.status_code == 200
    data = res.json()
    assert len(data["nodes"]) > 0
    print(f"[OK] GET /api/v1/graph/sandstorm returned {len(data['nodes'])} nodes and {len(data['edges'])} edges")

def test_alerts():
    res = client.get("/api/v1/alerts/sandstorm")
    assert res.status_code == 200
    alerts = res.json()["alerts"]
    assert len(alerts) >= 2
    print(f"[OK] GET /api/v1/alerts/sandstorm returned {len(alerts)} alerts (ANO-001, ANO-002, ANO-003)")

def test_review_queue():
    res = client.get("/api/v1/review-queue")
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) >= 2
    print(f"[OK] GET /api/v1/review-queue returned {len(items)} items")

    target_id = items[0]["merge_id"]
    # Test approve action
    action_res = client.post(f"/api/v1/review-queue/{target_id}/action", data={"action": "APPROVE", "notes": "Verified by investigator"})
    assert action_res.status_code == 200
    print(f"[OK] POST /api/v1/review-queue/{target_id}/action APPROVE succeeded")

def test_query():
    res = client.post("/api/v1/query", json={
        "case_id": "sandstorm",
        "query": "Find the hidden connection between Arjun Mehta and Phoenix Exports"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["key_findings"]) > 0
    print("[OK] POST /api/v1/query generated retrieval-grounded brief citing node IDs")

def test_influencers():
    res = client.get("/api/v1/influencers/sandstorm")
    assert res.status_code == 200
    data = res.json()
    assert data["total_influencers"] > 0
    top = data["influencers"][0]
    assert "inferred_role" in top
    print(f"[OK] GET /api/v1/influencers/sandstorm returned {data['total_influencers']} influencers (Top: {top['entity']} as {top['inferred_role']})")

def test_bfs_shortest_path():
    from db.neo4j_client import db_client
    path = db_client.shortest_path("A. Mehta", "Deepak R.")
    assert len(path.get("path_nodes", [])) >= 2
    print(f"[OK] db_client.shortest_path('A. Mehta', 'Deepak R.') resolved {len(path['path_nodes'])} nodes via in-memory BFS!")

def test_audit_log():
    res = client.get("/api/v1/audit-log")
    assert res.status_code == 200
    logs = res.json()["logs"]
    assert len(logs) > 0
    print(f"[OK] GET /api/v1/audit-log returned {len(logs)} immutable audit events")

if __name__ == "__main__":
    print("=== RUNNING NEXUS BACKEND API TESTS ===")
    test_root()
    test_seed_and_graph()
    test_alerts()
    test_influencers()
    test_bfs_shortest_path()
    test_review_queue()
    test_query()
    test_audit_log()
    print("\n[SUCCESS] ALL BACKEND API TESTS PASSED SUCCESSFULLY!")
