# 🎬 NEXUS v2.0 — 5-Minute Grand Finale Video Demo Script
### *Smart India Hackathon (SIH 2026) • Problem Statement: AI-Powered Criminal Network Analysis & Knowledge Graph*

---

## 📌 Executive Summary & Demo Strategy for Judges

| Segment | Target Time | Core Screen Focus | Key Metric / Tech to Highlight |
| :--- | :--- | :--- | :--- |
| **1. Hook & Problem Genesis** | 0:00 – 0:45 (45s) | Raw Ingestion / Dashboard Standby | 7,266 disparate records, cognitive overload, police backlog |
| **2. Multi-Agent Investigation** | 0:45 – 1:45 (60s) | Graph Canvas & Phase HUD | 4-agent consensus, 26 False Positives pruned, 0 False Accusations |
| **3. Deep Forensic Graph & Explainer** | 1:45 – 2:45 (60s) | Hover Tooltips & On-Canvas Badges | Directional edge badges, GNN PageRank, Betweenness Centrality |
| **4. Multi-Agent Debate & HITL** | 2:45 – 3:45 (60s) | Right Panel & HITL Review Modal | Resolver vs Extractor debate, BNSS Sec 111 alias ratification |
| **5. Natural Language & Court Dossier**| 3:45 – 4:30 (45s) | Natural Language Query & Dossier Modal | 28ms pathfinding traversal, Section 65B/63 BSA certified chargesheet |
| **6. Grand Closing & Scalability** | 4:30 – 5:00 (30s) | Case Switcher (Sandstorm ➔ Mirage) | Dockerized microservices, Neo4j, FastGraph traversal |

---

## ⏱️ Scene-by-Scene Screenplay & Narration

---

### 🕒 [0:00 – 0:45] SEGMENT 1: THE PROBLEM & RAW INGESTION

#### 🖥️ Visual on Screen:
* Start on **NEXUS v2.0 Dashboard** in **Raw Ingestion Standby** mode (`Operation Sandstorm`).
* The graph canvas displays muted, unanalyzed nodes with faint links.
* Left panel shows `RAW UNCLASSIFIED INGESTION (7,266 Records Ingested • 0 Pre-Judgments)`.
* Top status card shows `RAW INGESTION ACTIVE • 0% PROCESSED`.

#### 🎙️ Voiceover (Presenter):
> "Every single day, law enforcement agencies receive tens of thousands of fragmented evidence records: telecom Call Detail Records (CDRs), banking ledgers, mobile tower pings, and handwritten FIRs. 
> 
> Investigating officers spend weeks manually cross-referencing spreadsheets, leading to **two fatal failure modes**: criminal kingpins slipping through structural gaps, or innocent citizens being wrongfully implicated due to circumstantial overlap.
> 
> Meet **NEXUS v2.0** — an autonomous, multi-agent cyber intelligence command center that transforms raw, unclassified forensic telemetry into court-admissible, tamper-evident criminal syndicate graphs in milliseconds."

#### 🎯 What to Stress / Action:
* **Point out**: NEXUS starts in a forensic **Standby State**. It does **NOT** pre-judge people as suspects before running the AI pipeline.

---

### 🕒 [0:45 – 1:45] SEGMENT 2: MULTI-AGENT INVESTIGATION IN ACTION

#### 🖥️ Visual on Screen:
* Click the pulsing green button: **`Run AI Investigation`**.
* Watch the **Phase 1 ➔ Phase 2 ➔ Phase 3 ➔ Phase 4** execution live:
  * *Phase 1 (Probe)*: Faint yellow probe fires to noise node `N01`, detects lack of corroboration, flashes crimson, and dissolves.
  * *Phase 2 (Anomaly)*: Anomaly Radar highlights `[ANO-002: PMLA Cash Structuring]` and `[ANO-001: 18 Burst Calls]`.
  * *Phase 3 (GNN Scoring)*: Noise nodes deep fade; core syndicate illuminates with neon glows.
  * *Phase 4 (Consensus)*: Consensus meter hits **96.4%**, Top HUD announces `SYNDICATE ISOLATED (26 FP ELIMINATED • 0 FALSE ACCUSATIONS)`.

#### 🎙️ Voiceover (Presenter):
> "With one click, our multi-agent architecture takes over. 
> 
> Watch the screen: In **Phase 1**, our **Extractor Agent** probes candidate linkages across 7,266 raw records. A single misdialed civilian call is probed, refuted, and pruned in real time.
> 
> In **Phase 2**, our **Resolver Agent** matches anomaly patterns—detecting 10 structured banking deposits just below the ₹10 Lakh PMLA threshold and a burst of 18 encrypted calls preceding the contraband delivery.
> 
> In **Phase 3**, our **Graph Neural Network (GNN)** calculates PageRank and betweenness centrality, isolating the criminal core while filtering **26 ambient noise links**.
> 
> In **Phase 4**, the **Supervisor Agent** locks consensus at **96.4%**, guaranteeing zero false accusations under Bharatiya Sakshya Adhiniyam Section 63."

#### 🎯 What to Stress / Action:
* **Stress**: This is **TRUE Agentic AI** with deterministic guardrails—not just a generic single prompt LLM hallucinating names.

---

### 🕒 [1:45 – 2:45] SEGMENT 3: DEEP GRAPH FORENSICS & EXPLAINER AGENT

#### 🖥️ Visual on Screen:
* Point out the **Autorotating Directional On-Canvas Edge Badges**:
  * `10x ₹9.8L Smurfing` (Crimson vector from HDFC Account ➔ Phoenix Exports).
  * `18 Burst Calls` (Amber vector between burner phones).
  * `Controls Account`, `Dispatched Van MH-04-AZ-8812`, `Tower Co-location`.
* **Hover mouse over Node `Arjun Mehta`**:
  * The **`forensic-hover-card`** dialog pops up.
  * Point out:
    1. Role: `Prime Suspect (Core Syndicate)`
    2. Section: `⚙️ EXPLAINER AGENT FORENSIC VERDICT`
    3. Section: `🔀 ACTIVE RELATIONAL NEXUS` (Inflows & Outflows)
    4. Exhibit Citation: `fir_sandstorm_1.txt • PR=0.34 (Kingpin)`.
* **Test Interactive Mark/Clear**:
  * In left panel, select `Arjun Mehta` and click **`Clear / Innocent`** ➔ Node turns emerald green (`🟢`), edges dashed green.
  * Click **`Mark Suspect`** ➔ Node instantly turns neon crimson (`🚨`), edges flash red.

#### 🎙️ Voiceover (Presenter):
> "Look at the graph canvas. Unlike traditional black-box AI, every single edge in NEXUS renders **directional forensic badges** explaining the exact relationship—such as `10x ₹9.8L Smurfing` and `18 Burst Calls`.
> 
> When an investigator hovers over any entity, our embedded **Explainer Agent** generates an instant, multi-dimensional intelligence card detailing the exact *modus operandi*, incoming and outgoing cash flows, and the primary legal exhibit.
> 
> If new exculpatory evidence arises, the investigator retains full command: clicking **`Clear / Innocent`** immediately exonerates the citizen on the graph, maintaining human-in-the-loop integrity."

#### 🎯 What to Stress / Action:
* **Stress**: The **Explainer Agent** runs natively in real-time across the entire graph. No need to query external APIs or re-run models.

---

### 🕒 [2:45 – 3:45] SEGMENT 4: MULTI-AGENT DEBATE & HITL ALIAS RESOLUTION

#### 🖥️ Visual on Screen:
* Click on the **`Multi-Agent Debate`** tab in the right panel.
* Switch debate dispute topic to **`Alias Merging vs False Accusation`**.
* Show the live debate logs between **Extractor**, **Resolver**, **Analyst**, and **Supervisor**.
* Click **`HITL Review Queue`** button in the top navbar:
  * Review candidate: `Arjun Mehata` (FIR #0312) ↔ `Arjun Mehta` (FIR #0101) with Jaro-Winkler Similarity `89%`.
  * Click **`Approve`**.
  * Modal smoothly closes; the graph canvas **automatically zooms in** and renders a glowing emerald green vector with badge **`Ratified Alias Merge (BNSS 111)`**.

#### 🎙️ Voiceover (Presenter):
> "How does NEXUS prevent wrongful arrests? Through our **Multi-Agent Disputation Protocol**.
> 
> In the right panel, you can see our agents actively debating: the Extractor proposes linking 'Arjun Mehata' to 'Arjun Mehta'. The Resolver challenges with Jaro-Winkler string distance skepticism, and the Analyst corroborates shared CDR cell towers.
> 
> For ambiguous matches, NEXUS flags them into the **Human-in-the-Loop Review Queue** compliant with **BNSS Section 111**. 
> 
> Watch what happens when the lead investigator approves: the graph canvas immediately zooms in, dynamically generating a ratified alias link with an indelible cryptographic audit trail."

#### 🎯 What to Stress / Action:
* **Stress**: Compliance with modern Indian criminal laws (**BNS 2023**, **BNSS 2023**, and **BSA 2023**).

---

### 🕒 [3:45 – 4:30] SEGMENT 5: NATURAL LANGUAGE GRAPH TRAVERSAL & COURT DOSSIER

#### 🖥️ Visual on Screen:
* Switch to **`Evidence Brief`** tab in the right panel.
* Type or click query: `"How is Arjun Mehta connected to Phoenix Exports?"`
* Press Enter:
  * Latency badge updates to **`28ms`**.
  * Graph highlights the sub-network path (`Arjun Mehta ➔ HDFC Account ➔ Phoenix Exports`).
* Click **`Court Dossier`** button in the top navbar:
  * The formal legal chargesheet opens.
  * Scroll through:
    1. Five-Pillar Crime Breakdown Matrix.
    2. Evidence Exhibit Ledger (`fir_sandstorm_1.txt`, `txn_sandstorm.csv`).
    3. SHA-256 Cryptographic Hash & Digital Signature seal.
  * Click **`Print Dossier / Export PDF`** (shows clean print layout).

#### 🎙️ Voiceover (Presenter):
> "Investigating officers can query the criminal knowledge graph in plain conversational English. 
> 
> When we ask: *'How is Arjun Mehta connected to Phoenix Exports?'*, NEXUS performs sub-30 millisecond pathfinding traversal across Neo4j, illuminating the structured laundering pipeline.
> 
> Finally, when presenting evidence in court, NEXUS generates a complete, **Court-Admissible Dossier** formatted under Section 65B of the Indian Evidence Act and Section 63 of the BSA. It includes a 5-pillar crime breakdown, source hash verification, and the Investigating Officer's signature seal."

#### 🎯 What to Stress / Action:
* **Stress**: Sub-30ms execution speed, full citation fidelity, and print-ready legal admissibility.

---

### 🕒 [4:30 – 5:00] SEGMENT 6: MULTI-CASE SCALABILITY & CONCLUSION

#### 🖥️ Visual on Screen:
* Click the **Case Switcher dropdown** at the top right.
* Switch from `Operation Sandstorm (Narcotics)` ➔ `Operation Mirage (SIM-Swap Fraud)` or `Operation Phantom (Extortion & Hawala)`.
* Show that NEXUS instantly adapts its graph ontology, anomaly detectors, and statutory sections to any criminal typology.

#### 🎙️ Voiceover (Presenter):
> "NEXUS v2.0 is not limited to one scenario. With our plug-and-play Neo4j and Dockerized FastAPI architecture, NEXUS seamlessly scales across narcotics trafficking, night-time SIM-swap fraud, and corporate hawala rings.
> 
> By bridging cutting-edge Graph Neural Networks with agentic multi-agent consensus, NEXUS delivers unassailable forensic speed, protects innocent citizens, and empowers India's law enforcement for the cyber era.
> 
> Thank you."

---

## 💡 Top 5 Tips for the Pitch Team

1. **Be Punchy & Confident**: Speak with authoritative energy. Avoid long pauses while animations run; match your voice to the visual transitions.
2. **Show, Don't Just Tell**: Whenever you mention a feature (*"prunes 26 noise links"*, *"autorotating edge labels"*, *"BNSS Section 111"*), make sure your mouse or camera is highlighting that exact UI element.
3. **Emphasize Speed & Accuracy**: Emphasize **28ms latency**, **96.4% consensus**, and **0 false accusations**.
4. **Anticipate Jury Questions**:
   - *Q: Is this real AI or hardcoded?* ➔ A: It's an agentic multi-agent pipeline using IsolationForest, NetworkX/GDS centrality, and Jaro-Winkler string similarity with dynamic Neo4j path traversal.
   - *Q: Is it legally valid in Indian courts?* ➔ A: Yes, structured strictly according to BNS 2023, BNSS 2023, and BSA 2023 Section 63 / Evidence Act Section 65B.
5. **Keep Screen Clean**: Run in full-screen (`F11`) with clear 1080p resolution and smooth mouse movements.
