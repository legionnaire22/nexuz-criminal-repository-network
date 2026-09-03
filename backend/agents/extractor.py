"""
extractor.py
Agent 1: Extractor Agent (NEXUS v2.0)
Multi-tier hybrid extraction pipeline:
  Tier 1: High-precision deterministic Regex + structural FIR parsers
  Tier 2: OpenRouter LLM for unstructured narrative text & contextual roles
  Tier 3: Self-correction and relationship linking
"""

import re
import uuid
from typing import List, Dict, Any, Tuple, Optional
from schemas.canonical import ExtractedEntity, ExtractedRelation, IngestionBatch
from llm.openrouter_client import llm_client

# ── High-Precision Regular Expressions ───────────────────────────────────────
PHONE_REGEX = re.compile(r"\+91-[0-9]{5}-[0-9]{5}")
ACCOUNT_REGEX = re.compile(r"[A-Z]{3,5}-XXXX-[0-9]{4}")
VEHICLE_REGEX = re.compile(r"[A-Z]{2}-[0-9]{2}-[A-Z]{1,2}-[0-9]{4}")
TOWER_REGEX = re.compile(r"\b(?:BOM|BKC|MLW|SION)-[0-9]{3}\b")
SECTION_REGEX = re.compile(r"Section\s+[\d\-A-Za-z,\s]+(?:IPC|NDPS|PMLA|BNSS|IT Act|FEMA)", re.IGNORECASE)

ACCUSED_BLOCK_REGEX = re.compile(r"Accused No\.\s*\d+([\s\S]*?)(?=Accused No\.\s*\d+|\n\s*3\.|\n\s*═|$)", re.IGNORECASE)
NAME_FIELD_REGEX = re.compile(r"Name\s*:\s*([^\n\r]+)")
PHONE_FIELD_REGEX = re.compile(r"Phone\s*:\s*(\+91-[0-9]{5}-[0-9]{5})")
ROLE_FIELD_REGEX = re.compile(r"Role\s*:\s*([^\n\r]+)")
ALIAS_REGEX = re.compile(r"\[NOTE:\s*Alias\s*—\s*canon:\s*([^\]]+)\]", re.IGNORECASE)

KNOWN_ORGS = [
    "Phoenix Exports Pvt Ltd", "Phoenix Exports", "Phoenix Exp. Pvt Ltd", "Phoenix Exp.",
    "Sunrise Trading Co.", "Sunrise Traders",
    "Delta Finance Ltd", "Delta Finance", "Delta Fin. Ltd",
    "Sigma Holdings", "Sigma Hold.",
    "Apex Digital Services", "Apex Digital Svcs", "Apex Digital",
    "NextGen Solutions", "NextGen Sol."
]


class ExtractorAgent:
    def __init__(self):
        self.llm = llm_client

    def extract_from_fir(self, text: str, filename: str, case_id: str) -> IngestionBatch:
        """
        Extracts entities and relationships from free-text FIR.
        Combines deterministic regex extractions with OpenRouter LLM intelligence.
        """
        entities: List[ExtractedEntity] = []
        relations: List[ExtractedRelation] = []
        entity_map: Dict[str, str] = {}  # "Type:Value" -> entity_id

        def add_entity(etype: str, val: str, span: str = "", conf: float = 0.95, meta: dict = None) -> Optional[str]:
            val = val.strip().strip(",.;:")
            if not val or len(val) < 2:
                return None
            key = f"{etype}:{val}"
            if key in entity_map:
                return entity_map[key]
            eid = f"e_{uuid.uuid4().hex[:8]}"
            entity_map[key] = eid
            entities.append(ExtractedEntity(
                entity_id=eid,
                type=etype,
                value=val,
                source_doc=filename,
                raw_span=span or val,
                confidence=conf,
                metadata=meta or {}
            ))
            return eid

        # ── TIER 1: Deterministic Extraction from FIR Structure ──────────────────
        
        # 1. Phone Numbers
        for ph in PHONE_REGEX.findall(text):
            add_entity("Phone", ph, span=f"Phone {ph}", conf=1.0)

        # 2. Bank Accounts
        for acc in ACCOUNT_REGEX.findall(text):
            bank_name = acc.split("-")[0]
            add_entity("BankAccount", acc, span=f"Account {acc}", conf=1.0, meta={"bank": bank_name})

        # 3. Vehicles
        for veh in VEHICLE_REGEX.findall(text):
            add_entity("Vehicle", veh, span=f"Vehicle {veh}", conf=1.0)

        # 4. Cell Towers / Key Locations
        for tower in TOWER_REGEX.findall(text):
            add_entity("Location", tower, span=f"Tower {tower}", conf=1.0, meta={"is_tower": True})

        # 5. Organizations & Shell Companies
        for org in KNOWN_ORGS:
            if org in text:
                add_entity("Organization", org, span=org, conf=0.98, meta={"is_front": True})

        # 6. Parse Structured Accused Blocks
        accused_blocks = ACCUSED_BLOCK_REGEX.findall(text)
        suspect_ids = []

        for block in accused_blocks:
            name_match = NAME_FIELD_REGEX.search(block)
            phone_match = PHONE_FIELD_REGEX.search(block)
            veh_match = VEHICLE_REGEX.search(block)
            acc_match = ACCOUNT_REGEX.search(block)
            role_match = ROLE_FIELD_REGEX.search(block)
            alias_match = ALIAS_REGEX.search(block)

            p_id = None
            if name_match:
                raw_name = name_match.group(1).split("[")[0].strip()
                meta = {"is_suspect": True}
                if role_match:
                    meta["role"] = role_match.group(1).strip()
                if alias_match:
                    meta["canonical_hint"] = alias_match.group(1).strip()

                p_id = add_entity("Person", raw_name, span=block.strip()[:100], conf=0.95, meta=meta)
                if p_id:
                    suspect_ids.append(p_id)

            if p_id:
                # Link Person -> Phone (OWNS/USES)
                if phone_match:
                    ph_id = add_entity("Phone", phone_match.group(1), conf=1.0)
                    if ph_id:
                        relations.append(ExtractedRelation(
                            relation_type="OWNS",
                            source_entity_id=p_id,
                            target_entity_id=ph_id,
                            source_doc=filename,
                            weight=1.0,
                            confidence=0.98
                        ))

                # Link Person -> BankAccount (OWNS)
                if acc_match:
                    acc_id = add_entity("BankAccount", acc_match.group(0), conf=1.0)
                    if acc_id:
                        relations.append(ExtractedRelation(
                            relation_type="OWNS",
                            source_entity_id=p_id,
                            target_entity_id=acc_id,
                            source_doc=filename,
                            weight=1.0,
                            confidence=0.98
                        ))

                # Link Person -> Vehicle (OWNS)
                if veh_match:
                    veh_id = add_entity("Vehicle", veh_match.group(0), conf=1.0)
                    if veh_id:
                        relations.append(ExtractedRelation(
                            relation_type="OWNS",
                            source_entity_id=p_id,
                            target_entity_id=veh_id,
                            source_doc=filename,
                            weight=1.0,
                            confidence=0.95
                        ))

        # Connect Co-Accused within the same FIR
        for i in range(len(suspect_ids)):
            for j in range(i + 1, len(suspect_ids)):
                relations.append(ExtractedRelation(
                    relation_type="CO_ACCUSED",
                    source_entity_id=suspect_ids[i],
                    target_entity_id=suspect_ids[j],
                    source_doc=filename,
                    weight=1.0,
                    confidence=0.90
                ))

        # ── TIER 2: LLM Narrative Entity & Relational Extraction ────────────────
        # If narrative text contains unparsed details, prompt OpenRouter
        if self.llm and len(text) > 200:
            prompt = f"""
You are an expert Law Enforcement Entity Extraction Agent analyzing an official FIR narrative.
Extract all criminal entities and their connections from the text below.

FIR Text:
{text[:2500]}

Return STRICTLY valid JSON adhering to this schema:
{{
  "persons": [{{"name": "...", "role": "...", "is_suspect": true}}],
  "organizations": ["..."],
  "relations": [
    {{"source": "name/entity", "target": "name/entity", "relation": "MEMBER_OF | TRANSACTED_WITH | ASSOCIATED_WITH | LOCATED_AT"}}
  ]
}}
"""
            llm_res = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You are an expert Law Enforcement Intelligence Analyst. Always output strict JSON."
            )

            if llm_res and isinstance(llm_res, dict):
                # Ingest LLM Persons
                for p in llm_res.get("persons", []):
                    if isinstance(p, dict) and p.get("name"):
                        pid = add_entity("Person", p["name"], conf=0.90, meta={"role": p.get("role", ""), "is_suspect": p.get("is_suspect", True)})
                        if pid and pid not in suspect_ids and p.get("is_suspect"):
                            suspect_ids.append(pid)
                    elif isinstance(p, str):
                        add_entity("Person", p, conf=0.88, meta={"is_suspect": True})

                # Ingest LLM Organizations
                for org in llm_res.get("organizations", []):
                    if isinstance(org, str):
                        add_entity("Organization", org, conf=0.92)

                # Ingest LLM Relations
                for r in llm_res.get("relations", []):
                    if isinstance(r, dict) and r.get("source") and r.get("target"):
                        src_id = entity_map.get(f"Person:{r['source']}") or entity_map.get(f"Organization:{r['source']}")
                        tgt_id = entity_map.get(f"Person:{r['target']}") or entity_map.get(f"Organization:{r['target']}")
                        if src_id and tgt_id and src_id != tgt_id:
                            relations.append(ExtractedRelation(
                                relation_type=r.get("relation", "ASSOCIATED_WITH"),
                                source_entity_id=src_id,
                                target_entity_id=tgt_id,
                                source_doc=filename,
                                weight=1.0,
                                confidence=0.85
                            ))

        return IngestionBatch(case_id=case_id, entities=entities, relations=relations)

    def extract_from_cdr_rows(self, rows: List[Dict[str, Any]], filename: str, case_id: str) -> IngestionBatch:
        """Extract phones, locations, and call relations from CDR rows."""
        entities: List[ExtractedEntity] = []
        relations: List[ExtractedRelation] = []
        phone_map: Dict[str, str] = {}
        tower_map: Dict[str, str] = {}
        call_pairs: Dict[Tuple[str, str], Dict[str, Any]] = {}

        for r in rows:
            caller = r["caller_msisdn"].strip()
            callee = r["callee_msisdn"].strip()
            dur = int(r.get("duration_sec", 60))
            ts = r.get("start_timestamp", "")
            c_tower = r.get("caller_tower_id", "")

            # Ensure phone entities exist
            for ph in (caller, callee):
                if ph not in phone_map:
                    eid = f"ph_{uuid.uuid4().hex[:8]}"
                    phone_map[ph] = eid
                    entities.append(ExtractedEntity(
                        entity_id=eid,
                        type="Phone",
                        value=ph,
                        source_doc=filename,
                        confidence=1.0
                    ))

            # Ensure location/tower exists
            if c_tower and c_tower not in tower_map:
                tid = f"loc_{uuid.uuid4().hex[:8]}"
                tower_map[c_tower] = tid
                entities.append(ExtractedEntity(
                    entity_id=tid,
                    type="Location",
                    value=c_tower,
                    source_doc=filename,
                    confidence=1.0,
                    metadata={"lat": r.get("caller_tower_lat"), "lon": r.get("caller_tower_lon")}
                ))

            # Aggregate pair
            pair_key = (caller, callee)
            if pair_key not in call_pairs:
                call_pairs[pair_key] = {"count": 0, "total_dur": 0, "last_ts": ts}
            call_pairs[pair_key]["count"] += 1
            call_pairs[pair_key]["total_dur"] += dur
            if ts > call_pairs[pair_key]["last_ts"]:
                call_pairs[pair_key]["last_ts"] = ts

        # Create CALLED relations
        for (caller, callee), data in call_pairs.items():
            relations.append(ExtractedRelation(
                relation_type="CALLED",
                source_entity_id=phone_map[caller],
                target_entity_id=phone_map[callee],
                source_doc=filename,
                timestamp=data["last_ts"],
                weight=float(data["count"]),
                confidence=1.0,
                metadata={"call_count": data["count"], "total_duration_sec": data["total_dur"]}
            ))

        return IngestionBatch(case_id=case_id, entities=entities, relations=relations)

    def extract_from_txn_rows(self, rows: List[Dict[str, Any]], filename: str, case_id: str) -> IngestionBatch:
        """Extract accounts, names, and transaction relations from transaction rows."""
        entities: List[ExtractedEntity] = []
        relations: List[ExtractedRelation] = []
        acc_map: Dict[str, str] = {}
        name_map: Dict[str, str] = {}
        txn_pairs: Dict[Tuple[str, str], Dict[str, Any]] = {}

        for r in rows:
            s_acc = r["sender_account"].strip()
            r_acc = r["receiver_account"].strip()
            s_name = r["sender_name"].strip()
            r_name = r["receiver_name"].strip()
            amt = float(r.get("amount_inr", 0))
            ts = r.get("timestamp", "")

            # Ensure account entities exist
            for acc, bank in ((s_acc, r.get("sender_bank")), (r_acc, r.get("receiver_bank"))):
                if acc not in acc_map:
                    aid = f"acc_{uuid.uuid4().hex[:8]}"
                    acc_map[acc] = aid
                    entities.append(ExtractedEntity(
                        entity_id=aid,
                        type="BankAccount",
                        value=acc,
                        source_doc=filename,
                        confidence=1.0,
                        metadata={"bank": bank}
                    ))

            # Ensure person/entity names exist and connect to accounts
            for name, acc in ((s_name, s_acc), (r_name, r_acc)):
                if name and name not in name_map:
                    nid = f"p_{uuid.uuid4().hex[:8]}"
                    name_map[name] = nid
                    entities.append(ExtractedEntity(
                        entity_id=nid,
                        type="Person",
                        value=name,
                        source_doc=filename,
                        confidence=0.9
                    ))
                    relations.append(ExtractedRelation(
                        relation_type="OWNS",
                        source_entity_id=nid,
                        target_entity_id=acc_map[acc],
                        source_doc=filename,
                        confidence=0.95
                    ))

            # Aggregate transaction pairs
            pair_key = (s_acc, r_acc)
            if pair_key not in txn_pairs:
                txn_pairs[pair_key] = {"count": 0, "total_amt": 0.0, "last_ts": ts}
            txn_pairs[pair_key]["count"] += 1
            txn_pairs[pair_key]["total_amt"] += amt
            if ts > txn_pairs[pair_key]["last_ts"]:
                txn_pairs[pair_key]["last_ts"] = ts

        # Create TRANSACTED_WITH relations
        for (s_acc, r_acc), data in txn_pairs.items():
            relations.append(ExtractedRelation(
                relation_type="TRANSACTED_WITH",
                source_entity_id=acc_map[s_acc],
                target_entity_id=acc_map[r_acc],
                source_doc=filename,
                timestamp=data["last_ts"],
                weight=data["total_amt"],
                confidence=1.0,
                metadata={"txn_count": data["count"], "total_amount_inr": data["total_amt"]}
            ))

        return IngestionBatch(case_id=case_id, entities=entities, relations=relations)
