# NEXUS — Neo4j Graph Schema Contract
### SIH 2026 · Shared Schema Specification (Owned by P2)

---

## 1. Node Labels & Properties

Every node in NEXUS represents a resolved real-world entity or an unresolved candidate.

### Node Types

| Label | Key Identifier (`id`) | Example `name` / `value` | Core Properties |
|---|---|---|---|
| `:Person` | `P001`, `Q006`, or resolved UUID | "Arjun Mehta" | `canonical_id`, `name`, `aliases` (list), `role`, `confidence`, `is_suspect`, `source_docs` (list) |
| `:Phone` | Phone MSISDN e.g. `+91-98400-11111` | "+91-98400-11111" | `number`, `is_burner`, `carrier`, `source_docs` (list) |
| `:Organization` | `ORG001`, `ORG003` | "Phoenix Exports Pvt Ltd" | `name`, `aliases` (list), `is_shell_company`, `source_docs` (list) |
| `:BankAccount` | `ACC001`, `HDFC-XXXX-1001` | "HDFC-XXXX-1001" | `account_no`, `bank_name`, `source_docs` (list) |
| `:Location` | `LOC001`, `BOM-447` | "Dharavi, Mumbai" / Tower BOM-447 | `name`, `tower_id`, `lat`, `lon`, `source_docs` (list) |
| `:Vehicle` | `VEH001`, `MH-04-AB-1234` | "MH-04-AB-1234" | `reg_number`, `model`, `source_docs` (list) |

---

## 2. Relationship Types (Edges)

All edges must have `weight`, `confidence`, `source_docs`, and `last_updated`.

| Edge Type | Source Node -> Target Node | Key Properties | Description |
|---|---|---|---|
| `:CALLED` | `(:Phone) -> (:Phone)` | `call_count` (int), `total_duration_sec` (int), `last_timestamp` (datetime), `weights` | Aggregated call history |
| `:TRANSACTED_WITH` | `(:BankAccount) -> (:BankAccount)` or `(:Person) -> (:Person)` | `txn_count` (int), `total_amount_inr` (float), `latest_txn_date`, `is_anomalous` | Financial transaction link |
| `:CO_ACCUSED` | `(:Person) -> (:Person)` | `fir_nos` (list), `filing_date`, `sections` (list) | Co-accused in FIR |
| `:OWNS` / `:USES` | `(:Person) -> (:Phone\|:BankAccount\|:Vehicle)` | `confidence`, `verified_by_kyc` (bool) | Ownership or usage link |
| `:MEMBER_OF` | `(:Person) -> (:Organization)` | `role`, `is_director` (bool) | Affiliation or corporate role |
| `:LOCATED_AT` | `(:Phone\|:Person) -> (:Location)` | `timestamp`, `duration_min` | Tower ping or physical sighting |

---

## 3. Database Constraints & Indexes

Run these Cypher statements on Day 0:

```cypher
// Uniqueness Constraints
CREATE CONSTRAINT unique_person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.canonical_id IS UNIQUE;
CREATE CONSTRAINT unique_phone IF NOT EXISTS FOR (ph:Phone) REQUIRE ph.number IS UNIQUE;
CREATE CONSTRAINT unique_account IF NOT EXISTS FOR (b:BankAccount) REQUIRE b.account_no IS UNIQUE;
CREATE CONSTRAINT unique_org IF NOT EXISTS FOR (o:Organization) REQUIRE o.name IS UNIQUE;
CREATE CONSTRAINT unique_location IF NOT EXISTS FOR (l:Location) REQUIRE l.name IS UNIQUE;

// Fast Lookup Indexes
CREATE INDEX person_name_idx IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX phone_number_idx IF NOT EXISTS FOR (ph:Phone) ON (ph.number);
```

---

## 4. Neo4j Graph Data Science (GDS) Projections

GDS in-memory projection for running PageRank, Betweenness, Louvain, and Clustering Coefficient:

```cypher
// Create Graph Projection
CALL gds.graph.project(
  'nexusCrimeGraph',
  ['Person', 'Phone', 'BankAccount', 'Organization'],
  {
    CALLED: {orientation: 'UNDIRECTED', properties: 'weight'},
    TRANSACTED_WITH: {orientation: 'NATURAL', properties: 'total_amount_inr'},
    CO_ACCUSED: {orientation: 'UNDIRECTED'},
    OWNS: {orientation: 'UNDIRECTED'},
    MEMBER_OF: {orientation: 'UNDIRECTED'}
  }
);
```
