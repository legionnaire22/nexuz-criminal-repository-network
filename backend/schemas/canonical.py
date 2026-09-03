"""
canonical.py
Pydantic schemas for Extractor Agent output, graph representation, and API models.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ExtractedEntity(BaseModel):
    entity_id: str
    type: str  # Person, Phone, Location, Organization, Vehicle, BankAccount
    value: str
    source_doc: str
    raw_span: Optional[str] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExtractedRelation(BaseModel):
    relation_type: str  # CALLED, TRANSACTED_WITH, CO_ACCUSED, OWNS, MEMBER_OF, LOCATED_AT, ASSOCIATED_WITH
    source_entity_id: str
    target_entity_id: str
    source_doc: str
    timestamp: Optional[str] = None
    weight: float = 1.0
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestionBatch(BaseModel):
    case_id: str
    entities: List[ExtractedEntity]
    relations: List[ExtractedRelation]


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    is_suspect: bool = False
    role: Optional[str] = None
    pagerank_score: Optional[float] = None
    betweenness_score: Optional[float] = None
    community_id: Optional[int] = None
    aliases: List[str] = Field(default_factory=list)
    source_docs: List[str] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    weight: float = 1.0
    confidence: float = 1.0
    details: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class CytoscapeGraph(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class AnomalyAlert(BaseModel):
    alert_id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    layer: str     # Rule, Statistical, ML (IsolationForest), Graph-Structural (GDS)
    title: str
    description: str
    involved_entities: List[str]
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ReviewQueueItem(BaseModel):
    merge_id: str
    entity_1: Dict[str, Any]
    entity_2: Dict[str, Any]
    similarity_score: float
    match_reason: str
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED


class QueryRequest(BaseModel):
    case_id: str
    query: str


class QueryResponse(BaseModel):
    query: str
    plan_executed: List[str]
    summary: str
    key_findings: List[Dict[str, Any]]
    highlighted_subgraph: Dict[str, List[str]]
    confidence_score: float = 0.95
