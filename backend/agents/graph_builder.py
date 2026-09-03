"""
graph_builder.py
----------------
Agent 2: Graph Builder & Entity Resolver Agent (NEXUS v2.0)

Consolidated, self-contained implementation combining:
  1. Input & Resolved Pydantic Data Contracts
  2. Step 1: Exact Deduplication (Phones, Accounts, Vehicles, FIRs)
  3. Step 2 & 3: Fuzzy Name Matching (Jaro-Winkler) & Phonetic Filter (Soundex)
  4. Step 4: Cross-Field Multi-Signal Corroboration
  5. Step 5: Confidence Scoring Policy & Transitive Union-Find Merging
  6. Step 6: Knowledge Graph Construction (Neo4j MERGE & in-memory fallback)
  7. Human-in-the-Loop SQLite Review Queue (persistence & decisions)
  8. Adapter & Pipeline Runners for Agent 1 and Seeding
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import logging
import os
import re
import sqlite3
import uuid
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Set, Tuple

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from rapidfuzz.distance import JaroWinkler
from rapidfuzz.fuzz import token_sort_ratio, token_set_ratio

from db.neo4j_client import db_client

logger = logging.getLogger(__name__)

# Optional neo4j driver import
try:
    from neo4j import GraphDatabase
    HAS_NEO4J = True
except ImportError:
    HAS_NEO4J = False
    GraphDatabase = None


# ===========================================================================
# 1. ENUMERATIONS & DATA CONTRACTS
# ===========================================================================

class EntityType(str, Enum):
    PERSON = "PERSON"
    PHONE = "PHONE"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    ORGANIZATION = "ORGANIZATION"
    VEHICLE = "VEHICLE"
    LOCATION = "LOCATION"
    FIR = "FIR"


class CallType(str, Enum):
    VOICE = "VOICE"
    SMS = "SMS"
    DATA = "DATA"


class TxnType(str, Enum):
    IMPS = "IMPS"
    NEFT = "NEFT"
    RTGS = "RTGS"
    UPI = "UPI"
    CASH = "CASH"
    CHEQUE = "CHEQUE"
    OTHER = "OTHER"


class PersonRole(str, Enum):
    ACCUSED = "accused"
    COMPLAINANT = "complainant"
    WITNESS = "witness"
    UNKNOWN = "unknown"


class MergeStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_MERGED = "auto_merged"


class ExtractedEntity(BaseModel):
    """Raw entity extracted by Agent 1 (NER or regex)."""
    entity_id: str
    type: EntityType
    value: str
    source_doc: str
    source_type: Optional[str] = "fir"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, alias="extraction_confidence")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}

    @field_validator("confidence")
    @classmethod
    def round_confidence(cls, v: float) -> float:
        return round(v, 4)


class CDRRecord(BaseModel):
    """One row from a CDR CSV file."""
    call_id: str
    caller_msisdn: str
    callee_msisdn: str
    start_timestamp: str
    duration_sec: int = Field(default=60, ge=0)
    call_type: CallType = CallType.VOICE
    caller_tower_id: Optional[str] = None
    caller_tower_lat: Optional[float] = None
    caller_tower_lon: Optional[float] = None
    callee_tower_id: Optional[str] = None
    callee_tower_lat: Optional[float] = None
    callee_tower_lon: Optional[float] = None
    source_doc: str = ""
    case_name: str = ""

    @field_validator("caller_msisdn", "callee_msisdn", mode="before")
    @classmethod
    def normalize_msisdn(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)]", "", str(v))
        if cleaned.startswith("+91"):
            digits = cleaned[3:]
        elif cleaned.startswith("91") and len(cleaned) == 12:
            digits = cleaned[2:]
        elif cleaned.startswith("0"):
            digits = cleaned[1:]
        else:
            digits = cleaned
        if len(digits) == 10 and digits.isdigit():
            return f"+91{digits}"
        return cleaned


class TransactionRecord(BaseModel):
    """One row from a transaction CSV file."""
    txn_id: str
    sender_name: str
    sender_account: str
    sender_bank: str = ""
    receiver_name: str
    receiver_account: str
    receiver_bank: str = ""
    amount_inr: float = Field(..., gt=0)
    timestamp: str
    txn_type: TxnType = TxnType.OTHER
    reference_no: Optional[str] = None
    remarks: Optional[str] = None
    source_doc: str = ""
    case_name: str = ""


class Agent1Output(BaseModel):
    """Complete bundle received from Agent 1."""
    run_id: str
    case_name: str
    entities: List[ExtractedEntity] = Field(default_factory=list)
    cdr_records: List[CDRRecord] = Field(default_factory=list)
    txn_records: List[TransactionRecord] = Field(default_factory=list)
    processing_notes: List[str] = Field(default_factory=list)


class ResolvedEntity(BaseModel):
    """Canonical post-resolution entity ready for Neo4j."""
    canonical_id: str
    entity_type: EntityType
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    merged_from: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    normalized_msisdn: Optional[str] = None
    account_no: Optional[str] = None
    bank_name: Optional[str] = None
    plate_no: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tower_id: Optional[str] = None
    fir_no: Optional[str] = None
    police_station: Optional[str] = None
    case_name: Optional[str] = None
    bns_sections: List[str] = Field(default_factory=list)
    role: Optional[str] = None
    age: Optional[int] = None


class MergeSignal(BaseModel):
    signal_type: str
    weight: float
    score_contribution: float
    detail: str


class MergeCandidate(BaseModel):
    pair_id: str
    entity_a_id: str
    entity_a_value: str
    entity_a_source: str
    entity_b_id: str
    entity_b_value: str
    entity_b_source: str
    confidence_score: float
    signals: List[MergeSignal] = Field(default_factory=list)
    status: MergeStatus = MergeStatus.PENDING
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    reviewer_note: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def signal_summary(self) -> str:
        return "; ".join(s.detail for s in self.signals)


class ReviewDecision(BaseModel):
    action: str = Field(..., pattern="^(approve|reject|APPROVE|REJECT)$")
    reviewer_id: str = "Lead Investigator"
    note: Optional[str] = None


class ResolutionResult(BaseModel):
    run_id: str
    resolved_entities: List[ResolvedEntity]
    auto_merged_count: int = 0
    human_queue_count: int = 0
    kept_separate_count: int = 0
    total_input_entities: int = 0


# ===========================================================================
# 2. STEP 1: EXACT DEDUPLICATION
# ===========================================================================

def _normalize_msisdn_raw(raw: str) -> Optional[str]:
    cleaned = re.sub(r"[\s\-\(\)\+]", "", str(raw))
    if cleaned.startswith("91") and len(cleaned) == 12:
        digits = cleaned[2:]
    elif cleaned.startswith("0") and len(cleaned) == 11:
        digits = cleaned[1:]
    elif len(cleaned) == 10:
        digits = cleaned
    else:
        return None
    return f"+91{digits}" if digits.isdigit() else None


def _normalize_account_raw(raw: str) -> str:
    parts = raw.upper().strip().split("-")
    return f"{parts[0]}_{parts[-1]}" if len(parts) >= 3 else raw.upper().strip()


def _normalize_plate_raw(raw: str) -> str:
    return re.sub(r"[\s\-]", "", raw.upper().strip())


@dataclass
class DeduplicationResult:
    groups: Dict[str, List[str]] = field(default_factory=dict)
    entity_to_group: Dict[str, str] = field(default_factory=dict)

    def group_for(self, eid: str) -> str:
        return self.entity_to_group.get(eid, eid)


def run_exact_dedup(entities: List[ExtractedEntity]) -> DeduplicationResult:
    result = DeduplicationResult()
    phone_map: Dict[str, List[str]] = defaultdict(list)
    account_map: Dict[str, List[str]] = defaultdict(list)
    fir_map: Dict[str, List[str]] = defaultdict(list)
    vehicle_map: Dict[str, List[str]] = defaultdict(list)

    for ent in entities:
        eid = ent.entity_id
        if ent.type == EntityType.PHONE:
            k = _normalize_msisdn_raw(ent.value) or ent.value
            phone_map[k].append(eid)
        elif ent.type == EntityType.BANK_ACCOUNT:
            k = _normalize_account_raw(ent.metadata.get("account_no", ent.value))
            account_map[k].append(eid)
        elif ent.type == EntityType.FIR:
            k = ent.metadata.get("fir_no", ent.value)
            fir_map[k].append(eid)
        elif ent.type == EntityType.VEHICLE:
            k = _normalize_plate_raw(ent.metadata.get("plate_no", ent.value))
            vehicle_map[k].append(eid)
        else:
            result.groups[eid] = [eid]
            result.entity_to_group[eid] = eid

    for km in [phone_map, account_map, fir_map, vehicle_map]:
        for _, ids in km.items():
            if ids:
                ent_by_id = {e.entity_id: e for e in entities if e.entity_id in ids}
                leader = max(ids, key=lambda i: ent_by_id[i].confidence)
                result.groups[leader] = ids
                for i in ids:
                    result.entity_to_group[i] = leader

    return result


# ===========================================================================
# 3. STEPS 2 & 3: FUZZY MATCHING (JARO-WINKLER) & PHONETIC (SOUNDEX)
# ===========================================================================

def soundex(name: str) -> str:
    """Self-contained Soundex phonetic algorithm."""
    name = name.upper()
    name = "".join([c for c in name if c.isalpha()])
    if not name:
        return "0000"
    first = name[0]
    mapping = {"BFPV": "1", "CGJKQSXZ": "2", "DT": "3", "L": "4", "MN": "5", "R": "6"}
    code = ""
    for char in name[1:]:
        for key, val in mapping.items():
            if char in key:
                if not code or code[-1] != val:
                    code += val
                break
    code = code.replace("0", "")
    return (first + code + "000")[:4]


_TITLES_RE = re.compile(r"^(mr|mrs|ms|miss|dr|prof|shri|smt|kumari|late)\b\.?\s*", re.IGNORECASE)
_PUNCT_RE = re.compile(r"[.\-\'\",;:!?()]")


def _preprocess_name(name: str) -> str:
    name = name.strip()
    name = _TITLES_RE.sub("", name)
    name = _PUNCT_RE.sub("", name)
    return " ".join(name.split()).lower()


def _soundex_of(name: str) -> str:
    first_token = name.split()[0] if name.split() else name
    return soundex(first_token)


@dataclass
class FuzzyMatchPair:
    entity_a_id: str
    entity_a_value: str
    entity_b_id: str
    entity_b_value: str
    jaro_winkler_score: float
    soundex_match: bool
    source_a: str
    source_b: str


def run_fuzzy_match(
    entities: List[ExtractedEntity],
    jw_threshold: float = 0.88,
    require_soundex: bool = True,
) -> List[FuzzyMatchPair]:
    targets = [e for e in entities if e.type in (EntityType.PERSON, EntityType.ORGANIZATION)]
    if len(targets) < 2:
        return []

    preprocessed = {e.entity_id: _preprocess_name(e.value) for e in targets}
    soundex_codes = {eid: _soundex_of(n) for eid, n in preprocessed.items()}
    candidates: List[FuzzyMatchPair] = []

    for i in range(len(targets)):
        for j in range(i + 1, len(targets)):
            a = targets[i]
            b = targets[j]
            if a.entity_id == b.entity_id:
                continue
            na = preprocessed[a.entity_id]
            nb = preprocessed[b.entity_id]
            if na == nb:
                continue

            jw = JaroWinkler.normalized_similarity(na, nb)
            ts = token_sort_ratio(na, nb) / 100.0
            tset = token_set_ratio(na, nb) / 100.0
            sim = max(jw, ts, tset)

            if sim < jw_threshold:
                continue

            sx_match = (soundex_codes[a.entity_id] == soundex_codes[b.entity_id])
            if require_soundex and not sx_match:
                continue

            candidates.append(FuzzyMatchPair(
                entity_a_id=a.entity_id,
                entity_a_value=a.value,
                entity_b_id=b.entity_id,
                entity_b_value=b.value,
                jaro_winkler_score=round(sim, 4),
                soundex_match=sx_match,
                source_a=a.source_doc,
                source_b=b.source_doc,
            ))

    candidates.sort(key=lambda p: p.jaro_winkler_score, reverse=True)
    return candidates


# ===========================================================================
# 4. STEP 4: CROSS-FIELD CORROBORATION
# ===========================================================================

SIGNAL_WEIGHTS = {
    "exact_phone_match":     0.50,
    "exact_account_match":   0.45,
    "same_case_fir":         0.25,
    "fuzzy_name_match":      0.55,
    "phonetic_name_match":   0.15,
    "address_token_overlap": 0.15,
}

_ADDRESS_STOPWORDS = {
    "mumbai", "delhi", "india", "maharashtra", "road", "street", "nagar",
    "west", "east", "north", "south", "flat", "floor", "building", "colony",
    "society", "block", "lane", "cross", "sector", "phase", "plot",
}


@dataclass
class CorroboratedPair:
    entity_a_id: str
    entity_a_value: str
    entity_a_source: str
    entity_b_id: str
    entity_b_value: str
    entity_b_source: str
    confidence_score: float
    signals: List[MergeSignal] = field(default_factory=list)


def run_corroboration(
    entities: List[ExtractedEntity],
    fuzzy_pairs: List[FuzzyMatchPair],
) -> List[CorroboratedPair]:
    phone_map: Dict[str, Set[str]] = {}
    account_map: Dict[str, Set[str]] = {}
    for ent in entities:
        if ent.type == EntityType.PERSON:
            ph = set()
            if ent.metadata.get("normalized_msisdn"):
                ph.add(str(ent.metadata["normalized_msisdn"]))
            for p in ent.metadata.get("associated_phones", []):
                if p:
                    ph.add(str(p))
            phone_map[ent.entity_id] = ph

            acc = set()
            if ent.metadata.get("account_no"):
                acc.add(str(ent.metadata["account_no"]))
            account_map[ent.entity_id] = acc

    entity_index = {e.entity_id: e for e in entities}
    corroborated: List[CorroboratedPair] = []

    for pair in fuzzy_pairs:
        signals: List[MergeSignal] = []
        total = 0.0
        ea = entity_index.get(pair.entity_a_id)
        eb = entity_index.get(pair.entity_b_id)
        if not ea or not eb:
            continue

        # Signal 1: Name
        w_name = SIGNAL_WEIGHTS["fuzzy_name_match"]
        c_name = round(w_name * pair.jaro_winkler_score, 4)
        total += c_name
        signals.append(MergeSignal(
            signal_type="fuzzy_name_match",
            weight=w_name,
            score_contribution=c_name,
            detail=f"Jaro-Winkler({pair.entity_a_value!r}, {pair.entity_b_value!r}) = {pair.jaro_winkler_score:.3f}",
        ))

        # Signal 2: Soundex
        if pair.soundex_match:
            w_sx = SIGNAL_WEIGHTS["phonetic_name_match"]
            total += w_sx
            signals.append(MergeSignal(
                signal_type="phonetic_name_match",
                weight=w_sx,
                score_contribution=w_sx,
                detail=f"Soundex code match for '{pair.entity_a_value}' & '{pair.entity_b_value}'",
            ))

        # Signal 3: Phone
        shared_phones = phone_map.get(pair.entity_a_id, set()) & phone_map.get(pair.entity_b_id, set())
        if shared_phones:
            w_ph = SIGNAL_WEIGHTS["exact_phone_match"]
            total += w_ph
            signals.append(MergeSignal(
                signal_type="exact_phone_match",
                weight=w_ph,
                score_contribution=w_ph,
                detail=f"Shared phone(s): {', '.join(shared_phones)}",
            ))

        # Signal 4: Account
        shared_acc = account_map.get(pair.entity_a_id, set()) & account_map.get(pair.entity_b_id, set())
        if shared_acc:
            w_acc = SIGNAL_WEIGHTS["exact_account_match"]
            total += w_acc
            signals.append(MergeSignal(
                signal_type="exact_account_match",
                weight=w_acc,
                score_contribution=w_acc,
                detail=f"Shared account(s): {', '.join(shared_acc)}",
            ))

        # Signal 5: Source Doc
        if ea.source_doc == eb.source_doc:
            w_doc = SIGNAL_WEIGHTS["same_case_fir"]
            total += w_doc
            signals.append(MergeSignal(
                signal_type="same_case_fir",
                weight=w_doc,
                score_contribution=w_doc,
                detail=f"Both in document: {ea.source_doc}",
            ))

        total_score = min(round(total, 4), 1.0)
        corroborated.append(CorroboratedPair(
            entity_a_id=pair.entity_a_id,
            entity_a_value=pair.entity_a_value,
            entity_a_source=pair.source_a,
            entity_b_id=pair.entity_b_id,
            entity_b_value=pair.entity_b_value,
            entity_b_source=pair.source_b,
            confidence_score=total_score,
            signals=signals,
        ))

    corroborated.sort(key=lambda p: p.confidence_score, reverse=True)
    return corroborated


# ===========================================================================
# 5. STEP 5: CONFIDENCE SCORING & TRANSITIVE UNION-FIND POLICY
# ===========================================================================

AUTO_MERGE_THRESHOLD = 0.85
HUMAN_QUEUE_THRESHOLD = 0.60


class UnionFind:
    def __init__(self) -> None:
        self._parent: Dict[str, str] = {}

    def find(self, x: str) -> str:
        if x not in self._parent:
            self._parent[x] = x
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: str, y: str) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self._parent[ry] = rx

    def groups(self) -> Dict[str, List[str]]:
        res: Dict[str, List[str]] = {}
        for x in self._parent:
            r = self.find(x)
            res.setdefault(r, []).append(x)
        return res


def _make_canonical_id(etype: EntityType, name: str) -> str:
    key = f"{etype.value}::{name.lower().strip()}"
    digest = hashlib.sha256(key.encode()).hexdigest()[:12]
    return f"res_{etype.value.lower()}_{digest}"


def _pick_canonical_name(names: List[str]) -> str:
    def score(n: str) -> Tuple[int, int]:
        tokens = n.split()
        abbrev_pen = sum(1 for t in tokens if len(t) <= 2)
        return (-abbrev_pen, len(n))
    return max(names, key=score)


def apply_confidence_policy(
    entities: List[ExtractedEntity],
    corroborated_pairs: List[CorroboratedPair],
    dedup_result: DeduplicationResult,
    run_id: str,
) -> Tuple[ResolutionResult, List[MergeCandidate]]:
    entity_index = {e.entity_id: e for e in entities}
    uf = UnionFind()
    human_queue: List[MergeCandidate] = []
    auto_count = 0
    queue_count = 0
    separate_count = 0

    # Unconditional exact dedup groups
    for _, members in dedup_result.groups.items():
        if members:
            leader = members[0]
            for m in members:
                uf.union(leader, m)

    # Fuzzy & corroborated decisions
    for pair in corroborated_pairs:
        if pair.confidence_score >= AUTO_MERGE_THRESHOLD:
            uf.union(pair.entity_a_id, pair.entity_b_id)
            auto_count += 1
        elif pair.confidence_score >= HUMAN_QUEUE_THRESHOLD:
            human_queue.append(MergeCandidate(
                pair_id=f"pair_{uuid.uuid4().hex[:8]}",
                entity_a_id=pair.entity_a_id,
                entity_a_value=pair.entity_a_value,
                entity_a_source=pair.entity_a_source,
                entity_b_id=pair.entity_b_id,
                entity_b_value=pair.entity_b_value,
                entity_b_source=pair.entity_b_source,
                confidence_score=pair.confidence_score,
                signals=pair.signals,
                status=MergeStatus.PENDING,
            ))
            queue_count += 1
        else:
            separate_count += 1

    resolved_entities: List[ResolvedEntity] = []
    grouped_ids: Set[str] = set()

    for _, members in uf.groups().items():
        grouped_ids.update(members)
        m_entities = [entity_index[mid] for mid in members if mid in entity_index]
        if not m_entities:
            continue
        etype = m_entities[0].type
        aliases = list({e.value for e in m_entities})
        canon_name = _pick_canonical_name(aliases)
        sources = list({e.source_doc for e in m_entities})
        avg_conf = sum(e.confidence for e in m_entities) / len(m_entities)

        best = max(m_entities, key=lambda e: e.confidence)
        m = best.metadata

        resolved = ResolvedEntity(
            canonical_id=_make_canonical_id(etype, canon_name),
            entity_type=etype,
            canonical_name=canon_name,
            aliases=aliases,
            merged_from=[e.entity_id for e in m_entities],
            confidence=round(avg_conf, 4),
            sources=sources,
        )
        if etype == EntityType.PHONE:
            resolved.normalized_msisdn = m.get("normalized_msisdn", best.value)
        elif etype == EntityType.BANK_ACCOUNT:
            resolved.account_no = m.get("account_no", best.value)
            resolved.bank_name = m.get("bank_name")
        elif etype == EntityType.VEHICLE:
            resolved.plate_no = m.get("plate_no", best.value)
        elif etype == EntityType.LOCATION:
            resolved.lat = m.get("lat")
            resolved.lon = m.get("lon")
            resolved.tower_id = m.get("tower_id")
        elif etype == EntityType.FIR:
            resolved.fir_no = m.get("fir_no")
            resolved.police_station = m.get("police_station")
            resolved.bns_sections = m.get("bns_sections", [])
            resolved.case_name = m.get("case_name")
        elif etype == EntityType.PERSON:
            resolved.role = m.get("role")
            resolved.age = m.get("age")
            resolved.case_name = m.get("case_name")

        resolved_entities.append(resolved)

    for ent in entities:
        if ent.entity_id not in grouped_ids:
            resolved_entities.append(ResolvedEntity(
                canonical_id=_make_canonical_id(ent.type, ent.value),
                entity_type=ent.type,
                canonical_name=ent.value,
                aliases=[ent.value],
                merged_from=[ent.entity_id],
                confidence=ent.confidence,
                sources=[ent.source_doc],
            ))

    res = ResolutionResult(
        run_id=run_id,
        resolved_entities=resolved_entities,
        auto_merged_count=auto_count,
        human_queue_count=queue_count,
        kept_separate_count=separate_count,
        total_input_entities=len(entities),
    )
    return res, human_queue


# ===========================================================================
# 6. STEP 6: KNOWLEDGE GRAPH PERSISTENCE (NEO4J & IN-MEMORY)
# ===========================================================================

def _merge_neo4j_node(label: str, match_key: str, match_val: Any, props: Dict[str, Any]):
    if not HAS_NEO4J or not db_client.is_connected:
        return
    clean_props = {k: v for k, v in props.items() if v is not None}
    cypher = f"MERGE (n:{label} {{{match_key}: ${match_key}}}) SET n += $props"
    db_client.run_query(cypher, {match_key: match_val, "props": clean_props})


def _merge_neo4j_edge(
    from_label: str, from_key: str, from_val: Any,
    rel_type: str,
    to_label: str, to_key: str, to_val: Any,
    props: Dict[str, Any], merge_on: Optional[List[str]] = None,
):
    if not HAS_NEO4J or not db_client.is_connected:
        return
    clean_props = {k: v for k, v in props.items() if v is not None}
    if merge_on:
        merge_str = ", ".join(f"r.{k}: ${k}" for k in merge_on)
        set_str = ", ".join(f"r.{k} = ${k}" for k in clean_props if k not in merge_on)
        cypher = f"""
            MATCH (a:{from_label} {{{from_key}: $from_val}})
            MATCH (b:{to_label} {{{to_key}: $to_val}})
            MERGE (a)-[r:{rel_type} {{{merge_str}}}]->(b)
            {"SET " + set_str if set_str else ""}
        """
        params = {"from_val": from_val, "to_val": to_val, **clean_props}
    else:
        cypher = f"""
            MATCH (a:{from_label} {{{from_key}: $from_val}})
            MATCH (b:{to_label} {{{to_key}: $to_val}})
            MERGE (a)-[r:{rel_type}]->(b)
            SET r += $props
        """
        params = {"from_val": from_val, "to_val": to_val, "props": clean_props}
    db_client.run_query(cypher, params)


def upsert_graph_to_stores(
    resolved_entities: List[ResolvedEntity],
    cdr_records: List[CDRRecord],
    txn_records: List[TransactionRecord],
    merge_candidates: List[MergeCandidate],
    raw_entities: List[ExtractedEntity],
    sync_to_neo4j: bool = True,
) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Upsert canonical nodes and edges to Neo4j and the in-memory fallback client."""
    from itertools import combinations

    node_counts: Dict[str, int] = defaultdict(int)
    edge_counts: Dict[str, int] = defaultdict(int)

    raw_to_canon: Dict[str, str] = {}
    name_to_canon: Dict[str, str] = {}

    for e in resolved_entities:
        cid = e.canonical_id
        label = e.entity_type.value
        name = e.canonical_name
        node_counts[label] += 1

        for m_id in e.merged_from:
            raw_to_canon[m_id] = cid
        name_to_canon[name.lower()] = cid
        for al in e.aliases:
            name_to_canon[al.lower()] = cid

        # In-memory store
        db_client.upsert_node(
            node_id=cid,
            label=label,
            properties={
                "name": name,
                "aliases": e.aliases,
                "confidence": e.confidence,
                "sources": e.sources,
                "role": e.role,
                "case_name": e.case_name,
            }
        )
        # Neo4j
        if sync_to_neo4j:
            _merge_neo4j_node(
                label=label,
                match_key="canonical_id",
                match_val=cid,
                props={"canonical_id": cid, "canonical_name": name, "aliases": e.aliases, "confidence": e.confidence},
            )

    # CDR edges (CALLED, LOCATED_AT)
    for cdr in cdr_records:
        edge_counts["CALLED"] += 1
        db_client.upsert_edge(
            source_id=cdr.caller_msisdn,
            target_id=cdr.callee_msisdn,
            rel_type="CALLED",
            properties={"duration_sec": cdr.duration_sec, "timestamp": cdr.start_timestamp, "call_id": cdr.call_id},
        )
        if sync_to_neo4j:
            _merge_neo4j_edge(
                from_label="Phone", from_key="msisdn", from_val=cdr.caller_msisdn,
                rel_type="CALLED",
                to_label="Phone", to_key="msisdn", to_val=cdr.callee_msisdn,
                props={"call_id": cdr.call_id, "duration_sec": cdr.duration_sec, "timestamp": cdr.start_timestamp},
                merge_on=["call_id"],
            )

    # Transaction edges (TRANSACTED_WITH)
    for txn in txn_records:
        s_id = name_to_canon.get(txn.sender_name.lower(), txn.sender_account)
        r_id = name_to_canon.get(txn.receiver_name.lower(), txn.receiver_account)
        edge_counts["TRANSACTED_WITH"] += 1
        db_client.upsert_edge(
            source_id=s_id,
            target_id=r_id,
            rel_type="TRANSACTED_WITH",
            properties={"amount_inr": txn.amount_inr, "timestamp": txn.timestamp, "txn_id": txn.txn_id},
        )
        if sync_to_neo4j:
            _merge_neo4j_edge(
                from_label="Person", from_key="canonical_id", from_val=s_id,
                rel_type="TRANSACTED_WITH",
                to_label="Person", to_key="canonical_id", to_val=r_id,
                props={"txn_id": txn.txn_id, "amount_inr": txn.amount_inr, "timestamp": txn.timestamp},
                merge_on=["txn_id"],
            )

    # Accused co-occurrence edges (CO_ACCUSED)
    fir_accused: Dict[str, List[str]] = defaultdict(list)
    for ent in raw_entities:
        if ent.type == EntityType.PERSON and ent.metadata.get("role") == "accused":
            cid = raw_to_canon.get(ent.entity_id, ent.value)
            fir_accused[ent.source_doc].append(cid)

    for fir_doc, accused_list in fir_accused.items():
        for a, b in combinations(set(accused_list), 2):
            edge_counts["CO_ACCUSED"] += 1
            db_client.upsert_edge(
                source_id=a,
                target_id=b,
                rel_type="CO_ACCUSED",
                properties={"source_doc": fir_doc},
            )
            if sync_to_neo4j:
                _merge_neo4j_edge(
                    from_label="Person", from_key="canonical_id", from_val=a,
                    rel_type="CO_ACCUSED",
                    to_label="Person", to_key="canonical_id", to_val=b,
                    props={"source_doc": fir_doc},
                    merge_on=["source_doc"],
                )

    # Low-confidence review queue links (POSSIBLY_SAME_AS)
    for c in merge_candidates:
        edge_counts["POSSIBLY_SAME_AS"] += 1
        db_client.upsert_edge(
            source_id=c.entity_a_id,
            target_id=c.entity_b_id,
            rel_type="POSSIBLY_SAME_AS",
            properties={"pair_id": c.pair_id, "confidence": c.confidence_score, "status": c.status.value},
        )
        if sync_to_neo4j:
            _merge_neo4j_edge(
                from_label="Person", from_key="canonical_id", from_val=c.entity_a_id,
                rel_type="POSSIBLY_SAME_AS",
                to_label="Person", to_key="canonical_id", to_val=c.entity_b_id,
                props={"pair_id": c.pair_id, "confidence": c.confidence_score},
                merge_on=["pair_id"],
            )

    return dict(node_counts), dict(edge_counts)


# ===========================================================================
# 7. SQLITE HUMAN REVIEW QUEUE PERSISTENCE
# ===========================================================================

DB_PATH = os.getenv("NEXUS_SQLITE_PATH", "nexus_audit.db")

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS merge_candidates (
    pair_id         TEXT PRIMARY KEY,
    entity_a_id     TEXT NOT NULL,
    entity_a_value  TEXT NOT NULL,
    entity_a_source TEXT NOT NULL,
    entity_b_id     TEXT NOT NULL,
    entity_b_value  TEXT NOT NULL,
    entity_b_source TEXT NOT NULL,
    score           REAL NOT NULL,
    signals         TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    reviewed_by     TEXT,
    reviewed_at     TEXT,
    reviewer_note   TEXT,
    created_at      TEXT NOT NULL
);
"""


@contextmanager
def _get_sqlite_conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with _get_sqlite_conn() as conn:
        conn.execute(_CREATE_TABLE_SQL)


def save_candidates(candidates: List[MergeCandidate]) -> None:
    with _get_sqlite_conn() as conn:
        for c in candidates:
            conn.execute(
                """
                INSERT OR IGNORE INTO merge_candidates
                (pair_id, entity_a_id, entity_a_value, entity_a_source,
                 entity_b_id, entity_b_value, entity_b_source,
                 score, signals, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    c.pair_id, c.entity_a_id, c.entity_a_value, c.entity_a_source,
                    c.entity_b_id, c.entity_b_value, c.entity_b_source,
                    c.confidence_score, json.dumps([s.model_dump() for s in c.signals]),
                    c.status.value, c.created_at.isoformat(),
                ),
            )


def get_pending_candidates() -> List[Dict[str, Any]]:
    init_db()
    with _get_sqlite_conn() as conn:
        rows = conn.execute("SELECT * FROM merge_candidates WHERE status = 'pending' ORDER BY score DESC").fetchall()
    return [dict(r) for r in rows]


def get_candidate(pair_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    with _get_sqlite_conn() as conn:
        row = conn.execute("SELECT * FROM merge_candidates WHERE pair_id = ?", (pair_id,)).fetchone()
    return dict(row) if row else None


def apply_review_decision(pair_id: str, decision: ReviewDecision) -> bool:
    init_db()
    now = datetime.now(timezone.utc).isoformat()
    action = "approved" if decision.action.lower() == "approve" else "rejected"
    with _get_sqlite_conn() as conn:
        cur = conn.execute(
            """
            UPDATE merge_candidates
            SET status = ?, reviewed_by = ?, reviewed_at = ?, reviewer_note = ?
            WHERE pair_id = ? AND status = 'pending'
            """,
            (action, decision.reviewer_id, now, decision.note, pair_id),
        )
    return cur.rowcount > 0


# ===========================================================================
# 8. PIPELINE RUNNERS & INTERFACES
# ===========================================================================

def run_agent2_pipeline(
    input_data: Agent1Output,
    sync_to_neo4j: bool = True,
) -> Dict[str, Any]:
    """Execute the full 6-step Agent 2 Resolution and Graph Construction Pipeline."""
    run_id = input_data.run_id
    case_name = input_data.case_name
    entities = input_data.entities
    cdr_records = input_data.cdr_records
    txn_records = input_data.txn_records

    # 1. Init review DB
    init_db()

    # 2. Step 1: Dedup
    dedup = run_exact_dedup(entities)

    # 3. Steps 2 & 3: Fuzzy name & Soundex
    fuzzy_pairs = run_fuzzy_match(entities)

    # 4. Step 4: Corroboration
    corroborated = run_corroboration(entities, fuzzy_pairs)

    # 5. Step 5: Confidence policy & union-find
    resolution_res, merge_candidates = apply_confidence_policy(
        entities=entities,
        corroborated_pairs=corroborated,
        dedup_result=dedup,
        run_id=run_id,
    )

    # 6. Save human queue
    if merge_candidates:
        save_candidates(merge_candidates)

    # 7. Step 6: Upsert nodes & edges
    neo4j_status = "offline_in_memory_only"
    if sync_to_neo4j and HAS_NEO4J and db_client.is_connected:
        neo4j_status = "success"

    node_counts, edge_counts = upsert_graph_to_stores(
        resolved_entities=resolution_res.resolved_entities,
        cdr_records=cdr_records,
        txn_records=txn_records,
        merge_candidates=merge_candidates,
        raw_entities=entities,
        sync_to_neo4j=(neo4j_status == "success"),
    )

    return {
        "run_id": run_id,
        "case_name": case_name,
        "status": "completed",
        "total_input_entities": len(entities),
        "total_resolved_entities": len(resolution_res.resolved_entities),
        "auto_merged_count": resolution_res.auto_merged_count,
        "human_queue_count": resolution_res.human_queue_count,
        "kept_separate_count": resolution_res.kept_separate_count,
        "resolved_entities": [e.model_dump() for e in resolution_res.resolved_entities],
        "merge_candidates": [c.model_dump() for c in merge_candidates],
        "neo4j_status": neo4j_status,
        "node_counts": node_counts,
        "edge_counts": edge_counts,
    }


def agent2_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph state machine node function."""
    run_id = state.get("run_id", "langgraph_run")
    case_name = state.get("case_name", "all")

    raw_e = state.get("extracted_entities", [])
    raw_c = state.get("cdr_records", [])
    raw_t = state.get("txn_records", [])

    entities = [ExtractedEntity(**e) if isinstance(e, dict) else e for e in raw_e]
    cdrs = [CDRRecord(**c) if isinstance(c, dict) else c for c in raw_c]
    txns = [TransactionRecord(**t) if isinstance(t, dict) else t for t in raw_t]

    bundle = Agent1Output(
        run_id=run_id,
        case_name=case_name,
        entities=entities,
        cdr_records=cdrs,
        txn_records=txns,
    )

    res = run_agent2_pipeline(bundle, sync_to_neo4j=True)

    state["resolved_entities"] = res["resolved_entities"]
    state["human_review_queue"] = res["merge_candidates"]
    state["graph_node_counts"] = res["node_counts"]
    state["graph_edge_counts"] = res["edge_counts"]
    state["graph_ready"] = True
    state["agent2_summary"] = {
        "total_resolved": res["total_resolved_entities"],
        "auto_merged": res["auto_merged_count"],
        "pending_human_reviews": res["human_queue_count"],
        "neo4j_status": res["neo4j_status"],
    }
    return state


# ---------------------------------------------------------------------------
# Data Loader & Case Seeding Helpers
# ---------------------------------------------------------------------------

def _parse_fir_text_into_entities(filepath: str) -> List[ExtractedEntity]:
    entities: List[ExtractedEntity] = []
    fname = os.path.basename(filepath)
    source_doc = os.path.splitext(fname)[0]
    case_name = source_doc.split("_")[1] if "_" in source_doc else "unknown"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    fir_match = re.search(r"FIR No\s*:\s*([^\r\n]+)", content)
    fir_no = fir_match.group(1).strip() if fir_match else source_doc
    entities.append(ExtractedEntity(
        entity_id=f"fir_{source_doc}",
        type=EntityType.FIR,
        value=fir_no,
        source_doc=source_doc,
        confidence=1.0,
        metadata={"fir_no": fir_no, "case_name": case_name},
    ))

    accused_blocks = re.findall(
        r"Accused No\.\s*\d+.*?"
        r"Name\s*(?:\(stated\))?\s*:\s*([^\r\n\[]+)(?:\[NOTE:\s*Alias\s*–\s*canon:\s*([^\]]+)\])?.*?"
        r"(?:Address\s*:\s*([^\r\n]+).*?)?"
        r"(?:Vehicle\s*:\s*([^\r\n]+).*?)?"
        r"(?:Phone(?:\s*used)?\s*:\s*([^\r\n]+).*?)?"
        r"(?:Account\s*:\s*([^\r\n]+))?",
        content,
        re.DOTALL,
    )
    for i, (name, alias, addr, veh, phone, acct) in enumerate(accused_blocks, start=1):
        c_name = name.strip()
        c_phone = phone.strip() if phone else None
        c_acct = acct.strip() if acct else None
        c_veh = veh.strip() if veh else None

        entities.append(ExtractedEntity(
            entity_id=f"acc_{source_doc}_{i}",
            type=EntityType.PERSON,
            value=c_name,
            source_doc=source_doc,
            confidence=0.95,
            metadata={
                "role": "accused",
                "associated_phones": [c_phone] if c_phone else [],
                "account_no": c_acct,
                "case_name": case_name,
            },
        ))
        if c_phone:
            entities.append(ExtractedEntity(
                entity_id=f"ph_acc_{source_doc}_{i}",
                type=EntityType.PHONE,
                value=c_phone,
                source_doc=source_doc,
                confidence=1.0,
                metadata={"normalized_msisdn": c_phone},
            ))
        if c_acct:
            entities.append(ExtractedEntity(
                entity_id=f"acc_no_{source_doc}_{i}",
                type=EntityType.BANK_ACCOUNT,
                value=c_acct,
                source_doc=source_doc,
                confidence=1.0,
                metadata={"account_no": c_acct},
            ))
        if c_veh:
            entities.append(ExtractedEntity(
                entity_id=f"veh_acc_{source_doc}_{i}",
                type=EntityType.VEHICLE,
                value=c_veh,
                source_doc=source_doc,
                confidence=0.95,
                metadata={"plate_no": c_veh},
            ))

    return entities


def load_raw_dataset_bundle(
    raw_data_dir: str,
    case_filter: Optional[str] = None,
    max_cdrs: int = 500,
    max_txns: int = 500,
) -> Agent1Output:
    all_entities: List[ExtractedEntity] = []
    all_cdrs: List[CDRRecord] = []
    all_txns: List[TransactionRecord] = []

    # FIRs
    for fpath in glob.glob(os.path.join(raw_data_dir, "firs", "*.txt")):
        if case_filter and case_filter not in os.path.basename(fpath):
            continue
        all_entities.extend(_parse_fir_text_into_entities(fpath))

    # CDRs
    for cpath in glob.glob(os.path.join(raw_data_dir, "cdrs", "*.csv")):
        cname = os.path.basename(cpath)
        if case_filter and case_filter not in cname:
            continue
        case_name = cname.replace("cdr_", "").replace(".csv", "")
        with open(cpath, "r", encoding="utf-8") as f:
            for count, row in enumerate(csv.DictReader(f)):
                if count >= max_cdrs:
                    break
                try:
                    all_cdrs.append(CDRRecord(
                        call_id=row["call_id"],
                        caller_msisdn=row["caller_msisdn"],
                        callee_msisdn=row["callee_msisdn"],
                        start_timestamp=row["start_timestamp"],
                        duration_sec=int(row["duration_sec"]),
                        source_doc=os.path.splitext(cname)[0],
                        case_name=case_name,
                    ))
                except Exception:
                    continue

    # Transactions
    for tpath in glob.glob(os.path.join(raw_data_dir, "transactions", "*.csv")):
        tname = os.path.basename(tpath)
        if case_filter and case_filter not in tname:
            continue
        case_name = tname.replace("txn_", "").replace(".csv", "")
        with open(tpath, "r", encoding="utf-8") as f:
            for count, row in enumerate(csv.DictReader(f)):
                if count >= max_txns:
                    break
                try:
                    all_txns.append(TransactionRecord(
                        txn_id=row["txn_id"],
                        sender_name=row["sender_name"],
                        sender_account=row["sender_account"],
                        receiver_name=row["receiver_name"],
                        receiver_account=row["receiver_account"],
                        amount_inr=float(row["amount_inr"]),
                        timestamp=row["timestamp"],
                        source_doc=os.path.splitext(tname)[0],
                        case_name=case_name,
                    ))
                except Exception:
                    continue

    return Agent1Output(
        run_id=f"run_{case_filter or 'all'}",
        case_name=case_filter or "all",
        entities=all_entities,
        cdr_records=all_cdrs,
        txn_records=all_txns,
    )


def ingest_batch_to_agent2(batch, case_id: str, sync_to_neo4j: bool = True) -> Dict[str, Any]:
    """Compatibility adapter for Agent 1 Extractor output."""
    type_map = {
        "Person": EntityType.PERSON,
        "Phone": EntityType.PHONE,
        "BankAccount": EntityType.BANK_ACCOUNT,
        "Location": EntityType.LOCATION,
        "Organization": EntityType.ORGANIZATION,
        "Vehicle": EntityType.VEHICLE,
        "FIR": EntityType.FIR,
    }

    a2_entities = [
        ExtractedEntity(
            entity_id=e.entity_id,
            type=type_map.get(e.type, EntityType.PERSON),
            value=e.value,
            source_doc=e.source_doc,
            confidence=e.confidence,
            metadata=dict(e.metadata) if e.metadata else {},
        )
        for e in batch.entities
    ]

    bundle = Agent1Output(
        run_id=f"run_{case_id}",
        case_name=case_id,
        entities=a2_entities,
        cdr_records=[],
        txn_records=[],
    )
    return run_agent2_pipeline(bundle, sync_to_neo4j=sync_to_neo4j)


def load_and_run_case(
    case_id: str,
    data_dir: Optional[str] = None,
    sync_to_neo4j: bool = True,
    max_cdrs: int = 500,
    max_txns: int = 500,
) -> Dict[str, Any]:
    """Load and run the full case dataset across FIRs, CDRs, and Transactions."""
    if data_dir is None:
        agents_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(agents_dir)
        project_dir = os.path.dirname(backend_dir)
        data_dir = os.path.join(project_dir, "data", "raw")
        if not os.path.exists(data_dir):
            fallback = r"c:\Users\sudee\Desktop\SIH New\nexus\data\raw"
            if os.path.exists(fallback):
                data_dir = fallback

    bundle = load_raw_dataset_bundle(
        raw_data_dir=data_dir,
        case_filter=case_id,
        max_cdrs=max_cdrs,
        max_txns=max_txns,
    )
    res = run_agent2_pipeline(bundle, sync_to_neo4j=sync_to_neo4j)
    res["_bundle"] = bundle
    return res


# ===========================================================================
# 9. AGENT 2 API ROUTER
# ===========================================================================

router = APIRouter(prefix="/agent2", tags=["Agent 2: Graph Builder & Resolver"])


@router.post("/run", summary="Run Agent 2 Pipeline")
def api_run_agent2(payload: Agent1Output) -> Dict[str, Any]:
    return run_agent2_pipeline(payload, sync_to_neo4j=True)


@router.get("/review/queue", summary="Get Pending Human Review Merges")
def api_get_review_queue() -> List[Dict[str, Any]]:
    return get_pending_candidates()


@router.get("/review/{pair_id}", summary="Get Single Candidate Details")
def api_get_candidate(pair_id: str) -> Dict[str, Any]:
    cand = get_candidate(pair_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate pair not found")
    return cand


@router.post("/review/{pair_id}", summary="Submit Review Decision")
def api_submit_review_decision(pair_id: str, decision: ReviewDecision) -> Dict[str, Any]:
    success = apply_review_decision(pair_id, decision)
    if not success:
        raise HTTPException(status_code=400, detail="Candidate not found or not pending")
    return {"pair_id": pair_id, "action": decision.action, "status": "success"}


@router.get("/stats", summary="Get Graph & Resolver Statistics")
def api_get_stats() -> Dict[str, Any]:
    pending = len(get_pending_candidates())
    return {
        "nodes": len(db_client.in_memory_nodes),
        "edges": len(db_client.in_memory_edges),
        "pending_human_reviews": pending,
    }


# Singleton class interface for legacy/direct callers
class GraphBuilderAgent:
    def __init__(self):
        init_db()

    def resolve_and_build(self, batch) -> Dict[str, Any]:
        return ingest_batch_to_agent2(batch, case_id=batch.case_id)


graph_builder_agent = GraphBuilderAgent()
