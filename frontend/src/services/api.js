// API Client for FastAPI backend with fallback resilience

const API_BASE = "/api/v1";

export async function fetchReviewQueue() {
  try {
    const res = await fetch(`${API_BASE}/review-queue`, { signal: AbortSignal.timeout(2500) });
    if (res.ok) {
      const data = await res.json();
      return data.items || [];
    }
  } catch (e) {
    console.warn("Backend API offline, using local queue items.", e);
  }
  return null;
}

export async function postReviewDecision(mergeId, action, notes = "Decision ratified by Lead Investigator via Command UI") {
  try {
    const formData = new FormData();
    formData.append("action", action);
    formData.append("notes", notes);
    const res = await fetch(`${API_BASE}/review-queue/${mergeId}/action`, {
      method: "POST",
      body: formData,
      signal: AbortSignal.timeout(3000)
    });
    return res.ok;
  } catch (e) {
    console.warn("Backend API offline for decision action.", e);
    return false;
  }
}

export async function executeSupervisorQuery(caseId, query) {
  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ case_id: caseId, query: query }),
    signal: AbortSignal.timeout(4000)
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

export async function fetchCaseAlerts(caseId) {
  try {
    const res = await fetch(`${API_BASE}/alerts/${caseId}`, { signal: AbortSignal.timeout(2500) });
    if (res.ok) {
      const data = await res.json();
      return data.alerts || [];
    }
  } catch (e) {
    console.warn("Alerts API offline.", e);
  }
  return null;
}
