// Static Case Data & Graph Topologies for Offline & Live Scenarios

export const CASE_METADATA = {
  sandstorm: {
    title: "Operation Sandstorm",
    subtitle: "Narcotics Distribution, Hawala Smurfing & Burner SIM Ring",
    code: "NCR-2025-0312",
    fpRejected: 26,
    rawRecords: 7266,
    legal: {
      courtJurisdiction: "HON'BLE SPECIAL NDPS & PMLA COURT // GREATER MUMBAI SESSIONS DIVISION",
      statutorySections: "NDPS Act 1985 (Sec 22, 29) • PMLA 2002 (Sec 3, 4) • Bharatiya Nagarik Suraksha Sanhita (BNSS 2023 Sec 111)",
      exhibitsList: ["fir_sandstorm_1.txt", "fir_sandstorm_2.txt", "fir_sandstorm_3.txt", "cdr_sandstorm.csv", "txn_sandstorm.csv"],
      sha256: "8f4a2b91c0e35d72f1a8e9d4c2b7a1f5",
      terminalId: "NEXUS-NODE-MUM-NDPS-01",
      summaryNarrative: "FORENSIC CHARGESHEET NARRATIVE: Inter-agency investigation establishes that Arjun Mehta (Prime Accused / Syndicate Financier, PR=0.34) orchestrated an organized narcotics and money-laundering network operating across Mumbai and Nhava Sheva. Mehta coordinated logistics with Kabir Sheikh via 18 burst phone calls prior to seizure, corroborated through BTS co-location at Tower BKC-112. The syndicate structured ₹98,70,000 in illicit proceeds via 10 sub-threshold deposits (<₹10,00,000) into HDFC account ACC001, intentionally evading mandatory FIU-IND PMLA reporting thresholds. Layered funds were remitted into Phoenix Exports Pvt Ltd (corporate conduit directed by Anand Krishnan) and Axis Corporate accounts for offshore layering. Contraband transit was executed using seized transport van MH-04-AZ-8812 tracked at Nhava Sheva CFS. Burner SIM cards were procured without Aadhaar validation through Vikram Sinha's telecom franchise. All 26 ambient noise endpoints have been forensically pruned with zero false accusations under BSA Section 63.",
      breakdown: {
        genesis: "Arjun Mehta (Syndicate Financier / Kingpin) operated a high-volume narcotics procurement and distribution ring spanning Greater Mumbai and the Nhava Sheva container port zone. Contraband consignments were financed through structured hawala transfers and coordinated with field logistics coordinator Kabir Sheikh.",
        financialTrail: "PMLA Smurfing & Layering: The syndicate structured ₹98,70,000 across 10 discrete sub-threshold bank deposits (each ₹9,80,000–₹9,95,000) into HDFC account ACC001, deliberately evading mandatory ₹10 Lakh FIU-IND reporting thresholds. Funds were layered into Phoenix Exports Pvt Ltd (Current Acct directed by Anand Krishnan) and Axis Corporate accounts before off-ramp withdrawal by cash courier Deepak Rao.",
        telecomNexus: "Spatial & CDR Nexus: MSISDN +91-98400-11111 (Arjun Mehta) engaged in an abnormal burst of 18 calls within 48 hours to Kabir Sheikh (+91-98400-22222). Cellular triangulation confirmed concurrent BTS tower registration at Tower BKC-112 during contraband staging and transit.",
        seizures: "Physical & Asset Recoveries: Seized transport van (MH-04-AZ-8812) intercepted at Nhava Sheva CFS container freight station containing concealed contraband; 3 burner handsets seized; 10 corporate bank journals impounded.",
        pruningAudit: "Statutory & Pruning Audit: 26 ambient/civilian noise endpoints (grocery payments, utility bills, innocent bystander Dr. R. K. Verma) were algorithmically isolated and cleared with zero false accusations under BSA Section 63."
      }
    },
    suspects: [
      { id: "P001", name: "Arjun Mehta", alias: "A. Mehta / A.M.", role: "Syndicate Financier", score: 0.98, tags: ["PMLA STRUCTURING", "BKC-112 TOWER", "HAWALA HUB"], isSuspect: true, doc: "fir_sandstorm_1.txt", reason: "10 structured deposits <₹10L to Phoenix Exports; Primary MSISDN +91-98400-11111 active at raid site." },
      { id: "P002", name: "Kabir Sheikh", alias: "Kabeer", role: "Logistics Coordinator", score: 0.91, tags: ["CDR BURST", "BKC-112 TOWER"], isSuspect: true, doc: "fir_sandstorm_1.txt", reason: "18 burst calls prior to seizure; Co-located at Tower BKC-112 with Arjun Mehta." },
      { id: "P003", name: "Deepak Rao", alias: "D. Rao", role: "Hawala Courier", score: 0.88, tags: ["MULE ACCOUNT", "CASH WITHDRAWAL"], isSuspect: true, doc: "fir_sandstorm_2.txt", reason: "Executed rapid cash layering from HDFC-XXXX-1001; Named in FIR #0312 as courier." },
      { id: "P004", name: "Vikram Sinha", alias: "V. Sinha", role: "Telecom Distributor", score: 0.82, tags: ["BURNER SIM POOL", "IMEI SWAP"], isSuspect: false, doc: "fir_sandstorm_3.txt", reason: "Telecom franchise owner flagged for dispensing bulk unverified prepaid SIM cards." },
      { id: "P005", name: "Anand Krishnan", alias: "A. Krishnan", role: "Shell Entity Director", score: 0.79, tags: ["PHOENIX EXPORTS", "CURRENT ACCT"], isSuspect: false, doc: "fir_sandstorm_3.txt", reason: "Registered director of Phoenix Exports Pvt Ltd; Facilitated corporate banking conduit." },
      { id: "W001", name: "Dr. R. K. Verma", alias: "Eyewitness", role: "Innocent Bystander", score: 0.04, tags: ["WITNESS", "CLEARED"], isSuspect: false, doc: "fir_sandstorm_1.txt", reason: "Civilian medical practitioner present during search; Cleared of all criminal involvement." }
    ],
    alerts: [
      { id: "ANO-001", title: "Telecom CDR Burst Pattern", layer: "Layer 1 Heuristic", severity: "HIGH", detail: "18 calls within 48h pre-incident window between Arjun Mehta & logistics node." },
      { id: "ANO-002", title: "PMLA Cash Structuring (Smurfing)", layer: "Layer 1 Heuristic", severity: "CRITICAL", detail: "10 deposits of ₹9.80L–₹9.95L avoiding mandatory ₹10L FIU-IND reporting." },
      { id: "ANO-003", title: "Rapid Network Expansion", layer: "Layer 2 Graph", severity: "MEDIUM", detail: "Primary MSISDN +91-98400-11111 initiated contact with 4 new unknown numbers in 24h." }
    ],
    debateScenarios: {
      alias: [
        { agent: "Extractor", color: "extractor", time: "10:14:02", text: "Extracted raw accused alias 'A. Mehta' fleeing premises in FIR #0312. Proposing link to Arjun Mehta." },
        { agent: "Resolver", color: "resolver", time: "10:14:05", text: "Skepticism check: Jaro-Winkler string distance is 0.74. Applying BNSS Section 63 safeguards against false accusation." },
        { agent: "Analyst", color: "analyst", time: "10:14:09", text: "Corroboration confirmed: Phone +91-98400-11111 co-located at Tower BKC-112 with Arjun Mehta's bank login IP. PageRank 0.34 marks operational kingpin." },
        { agent: "Supervisor", color: "supervisor", time: "10:14:12", text: "Consensus Approved. Three-tier confidence reaches 96.4%. Canonical target auto-merged with zero false accusation." }
      ],
      role: [
        { agent: "Extractor", color: "extractor", time: "10:16:00", text: "Identified Anand Krishnan listed as company director in Phoenix Exports MCA registry." },
        { agent: "Analyst", color: "analyst", time: "10:16:04", text: "NetworkX PageRank is 0.15 (moderate), but betweenness centrality is 0.42. Node acts as conduit between legitimate bank transfers and mule couriers." },
        { agent: "Supervisor", color: "supervisor", time: "10:16:08", text: "Classification verified: Tagged as Corporate Shell Director rather than Operational Kingpin. Preserving evidence provenance." }
      ]
    },
    defaultBrief: {
      summary: "Arjun Mehta coordinates the primary narcotics and hawala distribution hub, laundering ₹98.7L through Phoenix Exports corporate conduit.",
      findings: [
        { text: "10 structured deposits of ₹9.80L–₹9.95L from HDFC-XXXX-1001 to Phoenix Exports corporate account [ANO-002].", nodes: ["P001", "ACC001", "ORG001"] },
        { text: "Abnormal CDR burst of 18 calls between MSISDN +91-98400-11111 and courier Deepak Rao prior to raid [ANO-001].", nodes: ["P001", "P003", "+91-98400-11111"] }
      ]
    }
  },
  phantom: {
    title: "Operation Phantom",
    subtitle: "Extortion Syndicate & Hidden Cross-Cluster Hawala Bridge",
    code: "NCR-2025-0198",
    fpRejected: 19,
    rawRecords: 4812,
    legal: {
      courtJurisdiction: "HON'BLE SPECIAL FINANCIAL CRIMES & EXTORTION TRIBUNAL // STATE SESSIONS",
      statutorySections: "Bharatiya Nyaya Sanhita (BNS 2023 Sec 308, 351) • IT Act 2000 (Sec 66D) • PMLA 2002 (Sec 3, 4)",
      exhibitsList: ["fir_phantom_1.txt", "fir_phantom_2.txt", "fir_phantom_4.txt", "cdr_phantom.csv", "txn_phantom.csv"],
      sha256: "7d9b3a12e5c84f61e2a9b4d3c1a8e7f2",
      terminalId: "NEXUS-NODE-FIN-EXT-02",
      summaryNarrative: "FORENSIC CHARGESHEET NARRATIVE: Multi-jurisdictional financial crime intelligence establishes an extortion-to-bullion money laundering pipeline operating through two segregated operational clusters. Cluster A, led by Vikram Sinha via Delta Finance Ltd, executed coercive extortion calls from MSISDN +91-97300-11111 against victims including Lakshmi Devi (Complainant, FIR #0198). Extorted proceeds collected in HDFC account ACC_DELTA were channeled to Anand Krishnan (Hidden Structural Broker, Betweenness Centrality=0.89, Clustering Coefficient < 0.05). Krishnan acted as the sole covert financial conduit, executing 6 round-number hawala transfers totaling ₹15,00,000 within 24 hours into Cluster B accounts controlled by Rohit Jain (Jain Bullion Traders). Illicit capital was liquidated into 2.8 kg of untraceable physical gold bullion through cashier Amitabh Shah. Graph isolation eliminated 19 civilian noise transactions, establishing 100% chain-of-custody corroboration under BNS Sec 308/351 and PMLA Sec 3/4.",
      breakdown: {
        genesis: "Vikram Sinha directed Delta Finance Ltd as a coercive extortion front, systematically threatening commercial targets and victims including complainant Lakshmi Devi (FIR #0198). Extortion calls were originated using VoIP and cellular gateways (+91-97300-11111).",
        financialTrail: "Cross-Cluster Hawala Laundering: Extorted collections gathered in HDFC-DELTA-8810 were funneled through Anand Krishnan (Hidden Structural Broker, Betweenness Centrality=0.89, Clustering Coefficient < 0.05). Krishnan routed 6 round-number transactions totaling ₹15,00,000 within 24 hours to Rohit Jain's accounts (SBI-JAIN-1092).",
        telecomNexus: "Coercive VoIP Routing: Coercive debt-recovery demands were coordinated by Neha Sharma and field enforcer Ravi Kumar, pinging Nariman Point financial district cell towers.",
        seizures: "Physical Gold Off-Ramp: Siphoned capital was converted into 2.8 kg of untraced physical bullion bars through Jain Bullion Traders, picked up by bullion cashier Amitabh Shah.",
        pruningAudit: "Statutory & Pruning Audit: 19 background transactions (independent software tenants, GST accounting fees, civilian retail purchases) pruned, securing 100% chain-of-custody corroboration under BNS Sec 308/351 and PMLA Sec 3/4."
      }
    },
    suspects: [
      { id: "Q006", name: "Anand Krishnan", alias: "A. Krishnan", role: "Hidden Cross-Cluster Bridge", score: 0.98, tags: ["STRUCTURAL BROKER", "LOW CLUSTERING"], isSuspect: true, doc: "fir_phantom_4.txt", reason: "Sole intermediary linking Extortion Cluster A to Laundering Cluster B." },
      { id: "Q001", name: "Vikram Sinha", alias: "V. Sinha", role: "Extortion Ring Leader (Cluster A)", score: 0.93, tags: ["EXTORTION CELL", "DELTA FINANCE"], isSuspect: true, doc: "fir_phantom_1.txt", reason: "Coordinated intimidation calls from +91-97300-11111 citing Delta Finance." },
      { id: "Q007", name: "Rohit Jain", alias: "R. Jain", role: "Hawala Recipient (Cluster B)", score: 0.89, tags: ["SMURFING RECEIVER", "SBI ACCT"], isSuspect: true, doc: "fir_phantom_2.txt", reason: "Received ₹15,00,000 in layered transfers forwarded through Anand Krishnan." },
      { id: "W002", name: "Lakshmi Devi", alias: "Complainant", role: "Extortion Victim", score: 0.02, tags: ["VICTIM", "CLEARED"], isSuspect: false, doc: "fir_phantom_1.txt", reason: "Victim who filed FIR #0198 after receiving extortion threats." }
    ],
    alerts: [
      { id: "ANO-004", title: "Hidden Structural Broker Discovered", layer: "Layer 4 GDS Graph", severity: "CRITICAL", detail: "Anand Krishnan identified as sole bridge linking extortion and laundering clusters." },
      { id: "ANO-005", title: "Round-Number Hawala Transfers", layer: "Layer 1 Rule", severity: "HIGH", detail: "6 transfers of exact amounts (₹5,00,000 & ₹10,00,000) between Delta Finance & Rohit Jain." }
    ],
    debateScenarios: {
      alias: [
        { agent: "Extractor", color: "extractor", time: "11:20:01", text: "Parsed FIR #0198 and 2 bank transaction journals. Identified 2 disparate operational clusters." },
        { agent: "Resolver", color: "resolver", time: "11:20:04", text: "Could Anand Krishnan be an unwitting retail accounting contractor? Testing betweenness centrality." },
        { agent: "Analyst", color: "analyst", time: "11:20:08", text: "GDS Betweenness Centrality is 0.89 with local clustering < 0.05. Funds forwarded to Rohit Jain within 90 minutes of extortion receipt." },
        { agent: "Supervisor", color: "supervisor", time: "11:20:12", text: "Confirmed active co-conspirator. Elevated to High Priority Target. Verified 100% citation fidelity across [Q006, Q001, Q007]." }
      ],
      role: [
        { agent: "Resolver", color: "resolver", time: "11:22:10", text: "Testing telecom clerk P. Desai culpability. Could this be clerical error?" },
        { agent: "Analyst", color: "analyst", time: "11:22:15", text: "Negative. Transaction timing shows funds forwarded to Rohit Jain within 90 minutes of extortion collection." },
        { agent: "Supervisor", color: "supervisor", time: "11:22:20", text: "Confirmed active co-conspirator. Elevated to High Priority Target." }
      ]
    },
    defaultBrief: {
      summary: "Anand Krishnan acts as the hidden structural bridge between Vikram Sinha's extortion cell (Delta Finance) and Rohit Jain's hawala laundering accounts.",
      findings: [
        { text: "Vikram Sinha directs Delta Finance Ltd, executing ₹10,00,000 hawala transfer to intermediary Anand Krishnan [ANO-004].", nodes: ["Q001", "ORG003", "Q006"] },
        { text: "Anand Krishnan routes 6 round-number transactions totaling ₹15,00,000 to Rohit Jain within 24h [ANO-005].", nodes: ["Q006", "Q007"] }
      ]
    }
  },
  mirage: {
    title: "Operation Mirage",
    subtitle: "Night-Time High-Velocity SIM-Swap Cyber Fraud Ring",
    code: "NCR-2025-0442",
    fpRejected: 31,
    rawRecords: 9450,
    legal: {
      courtJurisdiction: "HON'BLE CHIEF METROPOLITAN MAGISTRATE // CYBER & NARCOTICS DIVISION",
      statutorySections: "Information Technology Act 2000 (Sec 43, 66C, 66D) • Bharatiya Nyaya Sanhita (BNS 2023 Sec 318, 319)",
      exhibitsList: ["fir_mirage_1.txt", "fir_mirage_2.txt", "fir_mirage_3.txt", "cdr_mirage.csv", "txn_mirage.csv"],
      sha256: "4c8f1e92a3d75b61f0e4b8a2c7d9e1f5",
      terminalId: "NEXUS-NODE-CYBER-MUM-04",
      summaryNarrative: "FORENSIC CHARGESHEET NARRATIVE: Cyber-crime telemetry and cellular BTS audit establish a nocturnal high-velocity SIM-swap banking siphon. Prakash Desai (Telecom Franchise Insider) abused retail point-of-sale privileges to issue an unauthorized duplicate SIM for victim Alok Tandon (+91-96200-55555) using forged credentials. Spatial graph analysis confirmed co-location of 4 suspect handsets at Tower BKC-112 prior to execution. Between 02:00–04:00 AM, the syndicate intercepted net-banking 2FA OTPs and initiated 11 rapid transfers exceeding ₹9,00,000 to PNB and BOB mule accounts controlled by Imran Khan and Sunil Patil. Cash withdrawals totaling ₹2,50,000 were extracted at BKC and Kurla Station ATMs, while remaining proceeds were converted into USDT cryptocurrency via Binance P2P escrow (CRYPTO_01). Dark-web credential supplier Tariq Sheikh was linked via encrypted communications. Graph pruning eliminated 31 irrelevant cell-tower pings, sealing an unassailable digital evidence ledger under IT Act Sec 66C/66D and BNS Sec 318/319.",
      breakdown: {
        genesis: "Prakash Desai (telecom franchise retail insider) exploited authorized point-of-sale privileges to execute unauthorized SIM swaps without Aadhaar validation, cloning victim Alok Tandon's MSISDN (+91-96200-55555).",
        financialTrail: "Nocturnal High-Velocity Cyber Drain: Between 02:00–04:00 AM during SIM network blackout, the syndicate intercepted net-banking 2FA OTPs, executing 11 rapid transfers exceeding ₹9,00,000 into PNB and BOB student mule accounts managed by Imran Khan and Sunil Patil.",
        telecomNexus: "Multi-Suspect Tower Co-Location: 4 suspect handsets co-located at Tower BKC-112 immediately preceding the fraudulent porting request. Subsequent ATM extraction pings registered at Tower Kurla-W at 03:15 AM.",
        seizures: "Crypto Off-Ramp & ATM Seizures: ₹2,50,000 cash withdrawn from BKC and Kurla Station ATMs; ₹4,50,000 successfully converted to USDT cryptocurrency via Binance P2P escrow (CRYPTO_01); dark-web credential broker Tariq Sheikh identified.",
        pruningAudit: "Statutory & Pruning Audit: 31 civilian cell tower handoffs and support calls cleared with zero false accusations under IT Act Sec 66C/66D and BNS Sec 318/319."
      }
    },
    suspects: [
      { id: "M001", name: "Imran Khan", alias: "Imraan", role: "Primary Mule Coordinator", score: 0.97, tags: ["SIM CLONE", "PNB MULE"], isSuspect: true, doc: "fir_mirage_1.txt", reason: "Received fraudulent OTP-authenticated transfers of ₹9,00,000 during SIM outage." },
      { id: "M002", name: "Prakash Desai", alias: "P. Desai", role: "Telecom Insider Facilitator", score: 0.94, tags: ["UNAUTHORIZED SWAP", "TOWER BKC-112"], isSuspect: true, doc: "fir_mirage_2.txt", reason: "Issued duplicate SIM on forged Aadhaar; Co-located at Tower BKC-112." },
      { id: "M003", name: "Sunil Patil", alias: "S. Patil", role: "Mule Account Recruiter", score: 0.86, tags: ["4X SIM CARDS", "NIGHT WAVE"], isSuspect: true, doc: "fir_mirage_3.txt", reason: "Withdrew cash via ATMs between 02:00–04:00 AM immediately after SIM swap." }
    ],
    alerts: [
      { id: "ANO-006", title: "High-Value Night-Time Fraud Wave", layer: "Layer 3 IsolationForest", severity: "CRITICAL", detail: "11 transactions > ₹4,00,000 processed between 02:00–04:00 AM." },
      { id: "ANO-007", title: "Multi-Suspect Tower Co-Location", layer: "Layer 4 Spatial Graph", severity: "HIGH", detail: "4 suspect SIMs co-located at Tower BKC-112 preceding SIM clone execution." }
    ],
    debateScenarios: {
      alias: [
        { agent: "Extractor", color: "extractor", time: "14:02:11", text: "Processed victim statement from FIR #0442. Detected cloned MSISDN +91-96200-55555." },
        { agent: "Resolver", color: "resolver", time: "14:02:14", text: "Testing telecom clerk P. Desai culpability. Could this be inadvertent retail mistake?" },
        { agent: "Analyst", color: "analyst", time: "14:02:18", text: "Audit log reveals 4 duplicate SIM issuances within 30 minutes, all citing identical fabricated Aadhaar hash. Spatial co-location confirmed at Tower BKC-112." },
        { agent: "Supervisor", color: "supervisor", time: "14:02:22", text: "Conspiracy proven under BNS Sec 318 & IT Act Sec 66D. Accused status confirmed with 97% confidence." }
      ],
      role: [
        { agent: "Resolver", color: "resolver", time: "14:05:01", text: "Testing telecom clerk P. Desai culpability. Could this be clerical error?" },
        { agent: "Analyst", color: "analyst", time: "14:05:05", text: "Audit log reveals 4 duplicate SIM issuances within 30 minutes, all citing identical fabricated Aadhaar hash." },
        { agent: "Supervisor", color: "supervisor", time: "14:05:10", text: "Conspiracy proven under BNS Sec 318. Accused status confirmed." }
      ]
    },
    defaultBrief: {
      summary: "Prakash Desai (telecom insider) fraudulently cloned target SIM cards, enabling Imran Khan's mule accounts to siphon ₹9,00,000 during nocturnal hours.",
      findings: [
        { text: "Spatial co-location of 4 suspect handsets at Tower BKC-112 immediately preceding SIM swap [ANO-007].", nodes: ["M001", "M002", "TOW001"] },
        { text: "Night-time fraud wave: 11 rapid transfers exceeding ₹4,00,000 processed between 02:00–04:00 AM [ANO-006].", nodes: ["M001", "M003"] }
      ]
    }
  }
};

export const getFullGraphTopology = (caseId) => {
  if (caseId === "sandstorm") {
    return [
      // === Core Syndicate Targets & Brokers (Human Accused) ===
      { data: { id: "P001", label: "Arjun Mehta", icon: "🚨", size: 42, type: "target", doc: "fir_sandstorm_1.txt", metric: "PR=0.34 (Kingpin)", reason: "Named as core syndicate financier fleeing raid. Linked to HDFC-XXXX-1001 structuring ₹98.7L and phone +91-98400-11111." } },
      { data: { id: "P002", label: "Kabir Sheikh", icon: "🚨", size: 34, type: "target", doc: "fir_sandstorm_1.txt", metric: "PR=0.22 (Logistics)", reason: "18 burst calls prior to narcotics seizure; Co-located at Tower BKC-112 during delivery." } },
      { data: { id: "P003", label: "Deepak Rao", icon: "🚨", size: 30, type: "target", doc: "fir_sandstorm_2.txt", metric: "PR=0.18 (Courier)", reason: "Operated cash mule withdrawals from HDFC-XXXX-1001; Named in FIR #0312 as distributor." } },
      { data: { id: "P004", label: "Vikram Sinha", icon: "🟣", size: 28, type: "broker", doc: "fir_sandstorm_3.txt", metric: "PR=0.19 (SIM Vendor)", reason: "Telecom outlet owner who dispensed burner prepaid SIM cards used in contraband shipments." } },
      { data: { id: "P005", label: "Anand Krishnan", icon: "🟣", size: 28, type: "broker", doc: "fir_sandstorm_3.txt", metric: "PR=0.15 (Director)", reason: "Registered director of Phoenix Exports Pvt Ltd; Facilitated corporate bank conduit." } },
      
      // === Structured Assets, Accounts & Hardware ===
      { data: { id: "ACC001", label: "HDFC-XXXX-1001", icon: "💳", size: 24, type: "account", doc: "txn_sandstorm.csv", metric: "Txns: 10 Sub-Threshold", reason: "Account executing structured transfers under ₹10L to evade PMLA reporting." } },
      { data: { id: "ACC002", label: "ICICI-MULE-4491", icon: "💳", size: 22, type: "account", doc: "txn_sandstorm.csv", metric: "Cash Drain Mule", reason: "Secondary account receiving cash deposits for courier Deepak Rao." } },
      { data: { id: "ACC003", label: "AXIS-CORP-9920", icon: "💳", size: 22, type: "account", doc: "txn_sandstorm.csv", metric: "Layering Conduit", reason: "Axis corporate current account forwarding offshore remittances." } },
      { data: { id: "ORG001", label: "Phoenix Exports", icon: "🏢", size: 34, type: "organization", doc: "fir_sandstorm_3.txt", metric: "Shell Corp Conduit", reason: "Front company receiving layered funds used to finance cross-border narcotics shipments." } },
      { data: { id: "ORG002", label: "OceanGate Freight", icon: "🏢", size: 24, type: "organization", doc: "fir_sandstorm_2.txt", metric: "Customs Clearing", reason: "Logistics partner cleared for handling container manifest." } },
      { data: { id: "PH001", label: "+91-98400-11111", icon: "📱", size: 22, type: "phone", doc: "cdr_sandstorm.csv", metric: "Tower: BKC-112", reason: "Primary cellular handset monitored during narcotics raid window." } },
      { data: { id: "PH002", label: "+91-98400-22222", icon: "📱", size: 22, type: "phone", doc: "cdr_sandstorm.csv", metric: "Calls: 18 Burst", reason: "Burner mobile phone maintained by logistics coordinator Kabir Sheikh." } },
      { data: { id: "PH003", label: "+91-98400-33333", icon: "📱", size: 20, type: "phone", doc: "cdr_sandstorm.csv", metric: "Burner Phone 3", reason: "Dispatched burner phone used by courier Deepak Rao." } },
      { data: { id: "VEH001", label: "Van MH-04-AZ-8812", icon: "🚐", size: 24, type: "vehicle", doc: "fir_sandstorm_1.txt", metric: "Seized Transport Asset", reason: "Seized transport vehicle containing concealed contraband consignment." } },
      { data: { id: "LOC001", label: "Nhava Sheva CFS", icon: "📍", size: 24, type: "location", doc: "fir_sandstorm_2.txt", metric: "Seizure Location", reason: "Port freight station where contraband shipment was staged." } },
      { data: { id: "TOW001", label: "Tower BKC-112", icon: "📡", size: 26, type: "tower", doc: "cdr_sandstorm.csv", metric: "Co-location Hub", reason: "Cellular tower where Arjun Mehta & Kabir Sheikh handsets co-occurred." } },
      { data: { id: "TOW002", label: "Tower Colaba-04", icon: "📡", size: 22, type: "tower", doc: "cdr_sandstorm.csv", metric: "Transit Cell Tower", reason: "Intermediate tower logging movement between 20:00–21:30." } },
      { data: { id: "TOW003", label: "Tower JNPT-09", icon: "📡", size: 22, type: "tower", doc: "cdr_sandstorm.csv", metric: "Port Access Tower", reason: "Cell tower covering Nhava Sheva CFS gateway." } },
      { data: { id: "W001", label: "Dr. R.K. Verma", icon: "🟢", size: 24, type: "cleared", doc: "fir_sandstorm_1.txt", metric: "Eyewitness (Cleared)", reason: "Independent civilian witness to raid; Cleared with zero criminal associations." } },
      
      // === Dense Candidate Background & Noise Field (Filtering 7,266 Raw Records) ===
      { data: { id: "N01", label: "98200-XXXX1", icon: "📱", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "CDR Misdial", reason: "Casual single-call interaction during daytime; Zero criminal co-location." } },
      { data: { id: "N02", label: "98200-XXXX2", icon: "📱", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "Normal Traffic", reason: "Delivery courier service call; No recurrent interaction." } },
      { data: { id: "N03", label: "Metro Dairy", icon: "🧾", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Retail UPI ₹450", reason: "Legitimate grocery vendor transaction; Cleared automatically by IsolationForest." } },
      { data: { id: "N04", label: "Apex Stationary", icon: "🧾", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Retail UPI ₹1,200", reason: "Office supply vendor payee; Non-smurfing round transaction." } },
      { data: { id: "N05", label: "98200-XXXX3", icon: "📱", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "Tower Andheri-E", reason: "Call pinged unrelated tower; No geographic tie to seizure site." } },
      { data: { id: "N06", label: "Suresh Mehta", icon: "👤", size: 18, type: "noise", doc: "fir_sandstorm_1.txt", metric: "Kinsman (Cleared)", reason: "Accused's father named in FIR header; Zero involvement in syndicate operations." } },
      { data: { id: "N07", label: "QuickPay", icon: "⚡", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Utility Payee", reason: "Telecom top-up merchant; Cleared of money laundering." } },
      { data: { id: "N08", label: "Pooja Mehta", icon: "👤", size: 16, type: "noise", doc: "fir_sandstorm_1.txt", metric: "Family Contact", reason: "Kinship call record; No financial or logistics activity." } },
      { data: { id: "N09", label: "Swiggy Delivery", icon: "🍔", size: 14, type: "noise", doc: "txn_sandstorm.csv", metric: "UPI Merchant ₹620", reason: "Routine personal food order payee." } },
      { data: { id: "N10", label: "HPCL Petrol", icon: "🚗", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Fuel Card ₹2,500", reason: "Standard vehicle refuel transaction." } },
      { data: { id: "N11", label: "Apollo Pharmacy", icon: "🏥", size: 14, type: "noise", doc: "txn_sandstorm.csv", metric: "Retail POS ₹890", reason: "Medical prescription purchase." } },
      { data: { id: "N12", label: "Uber India", icon: "🚗", size: 14, type: "noise", doc: "txn_sandstorm.csv", metric: "Mobility Fare ₹340", reason: "Legitimate commuter trip log." } },
      { data: { id: "N13", label: "Tata Power", icon: "⚡", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Electricity ₹4,200", reason: "Routine residential bill auto-debit." } },
      { data: { id: "N14", label: "Sunita Rao", icon: "👤", size: 16, type: "noise", doc: "fir_sandstorm_2.txt", metric: "Spouse (Cleared)", reason: "Deepak Rao's spouse; Verified independent salary account." } },
      { data: { id: "N15", label: "Ramesh CA", icon: "💼", size: 17, type: "noise", doc: "fir_sandstorm_3.txt", metric: "Statutory Auditor", reason: "Chartered accountant who certified annual balance sheet." } },
      { data: { id: "N16", label: "Tower Dadar-C", icon: "📡", size: 18, type: "noise", doc: "cdr_sandstorm.csv", metric: "Transit Tower", reason: "Common suburban cellular repeater." } },
      { data: { id: "N17", label: "Tower Andheri-W", icon: "📡", size: 18, type: "noise", doc: "cdr_sandstorm.csv", metric: "Daytime Tower", reason: "Commercial office zone cell tower." } },
      { data: { id: "N18", label: "98330-XXXX7", icon: "📱", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "SMS Alert", reason: "Bank automated OTP notifications." } },
      { data: { id: "N19", label: "98330-XXXX8", icon: "📱", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "Spam Telemarketer", reason: "Insurance marketing outbound call." } },
      { data: { id: "N20", label: "FastTrack Log", icon: "📦", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Courier Fee ₹210", reason: "Independent freight booking for domestic parcels." } },
      { data: { id: "N21", label: "Canteen Hub", icon: "☕", size: 14, type: "noise", doc: "txn_sandstorm.csv", metric: "Lunch UPI ₹180", reason: "Office canteen meal charge." } },
      { data: { id: "N22", label: "Security Guard", icon: "👤", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "Guard Tower Log", reason: "Gate security personnel on duty at industrial complex." } },
      { data: { id: "N23", label: "State Bank Pen", icon: "💳", size: 15, type: "noise", doc: "txn_sandstorm.csv", metric: "Pension Credit", reason: "Senior citizen monthly retirement disbursement." } },
      { data: { id: "N24", label: "Post Office", icon: "🏢", size: 14, type: "noise", doc: "txn_sandstorm.csv", metric: "Postal Deposit", reason: "Personal recurring deposit savings." } },
      { data: { id: "N25", label: "Railway Ping", icon: "🚇", size: 14, type: "noise", doc: "cdr_sandstorm.csv", metric: "Transit Cell Ping", reason: "Suburban railway passenger cell ping." } },

      // === Verified Criminal Syndicate Edges ===
      { data: { id: "e1", source: "P001", target: "ACC001", rel_type: "CONTROLS_ACCOUNT", rel_label: "Controls Account", weight: 4.5, color: "#ff2a55", doc: "txn_sandstorm.csv", metric: "Signatory Authority", reason: "Direct signatory control and beneficiary authority over HDFC account." } },
      { data: { id: "e2", source: "ACC001", target: "ORG001", rel_type: "PMLA_SMURFING", rel_label: "10x ₹9.8L Smurfing", weight: 4.5, color: "#ff2a55", doc: "txn_sandstorm.csv", metric: "10x ₹9.80L Deposits", reason: "ANO-002: 10 structured transfers under ₹10L threshold routed into corporate shell account." } },
      { data: { id: "e3", source: "P001", target: "PH001", rel_type: "SUBSCRIBER_OF", rel_label: "Subscriber", weight: 3, color: "#00f0ff", doc: "cdr_sandstorm.csv", metric: "MSISDN Match", reason: "Telecom registration and CDR tower logs confirm active ownership of +91-98400-11111." } },
      { data: { id: "e4", source: "PH001", target: "PH002", rel_type: "CDR_BURST_CALLS", rel_label: "18 Burst Calls", weight: 4.5, color: "#ffb800", doc: "cdr_sandstorm.csv", metric: "18 Calls in 48h", reason: "ANO-001: Abnormal spike of 18 phone calls immediately preceding the narcotics delivery." } },
      { data: { id: "e5", source: "PH002", target: "P002", rel_type: "USED_BY", rel_label: "Handset Used", weight: 3, color: "#00f0ff", doc: "fir_sandstorm_1.txt", metric: "Device Seized", reason: "Burner phone recovered directly from Kabir Sheikh upon apprehension." } },
      { data: { id: "e6", source: "P002", target: "P003", rel_type: "CO_ACCUSED", rel_label: "Co-Accused", weight: 3, color: "#ff7b95", doc: "fir_sandstorm_2.txt", metric: "Named Jointly", reason: "Jointly indicted under NDPS Sections 22 & 29 in FIR #0312." } },
      { data: { id: "e7", source: "P005", target: "ORG001", rel_type: "DIRECTOR_OF", rel_label: "MCA Director", weight: 3, color: "#a855f7", doc: "fir_sandstorm_3.txt", metric: "MCA21 Registry", reason: "Official corporate filings list Anand Krishnan as statutory director of Phoenix Exports." } },
      { data: { id: "e8", source: "P004", target: "PH002", rel_type: "DISPENSED_SIM", rel_label: "Dispensed SIM", weight: 2.5, color: "#a855f7", doc: "fir_sandstorm_3.txt", metric: "Retailer Point-of-Sale", reason: "Prepaid SIM card activated at Vikram Sinha's telecom outlet without Aadhaar validation." } },
      { data: { id: "e9", source: "P004", target: "PH003", rel_type: "DISPENSED_SIM", rel_label: "Burner Pool SIM", weight: 2.5, color: "#a855f7", doc: "fir_sandstorm_3.txt", metric: "Burner Pool", reason: "Secondary burner SIM activated using forged customer application form." } },
      { data: { id: "e10", source: "P003", target: "PH003", rel_type: "CARRIED_DEVICE", rel_label: "Courier Handset", weight: 2.5, color: "#00f0ff", doc: "fir_sandstorm_2.txt", metric: "Active Device", reason: "Handset located in possession of courier Deepak Rao." } },
      { data: { id: "e11", source: "P001", target: "TOW001", rel_type: "TOWER_PING", rel_label: "Tower Co-location", weight: 3, color: "#ffb800", doc: "cdr_sandstorm.csv", metric: "Co-located", reason: "Tower BKC-112 recorded subscriber connection during raid prep." } },
      { data: { id: "e12", source: "P002", target: "TOW001", rel_type: "TOWER_PING", rel_label: "Tower Co-location", weight: 3, color: "#ffb800", doc: "cdr_sandstorm.csv", metric: "Co-located", reason: "Concurrent cell tower registration verifying rendezvous." } },
      { data: { id: "e13", source: "P003", target: "ACC002", rel_type: "OPERATES_MULE", rel_label: "Cash Mule Drain", weight: 3, color: "#ff2a55", doc: "txn_sandstorm.csv", metric: "Mule Cashier", reason: "Cash withdrawals executed immediately upon receipt of transfers." } },
      { data: { id: "e14", source: "ORG001", target: "ACC003", rel_type: "TRANSFERS_TO", rel_label: "Layering Remittance", weight: 3.5, color: "#ff2a55", doc: "txn_sandstorm.csv", metric: "Layering Flight", reason: "Inter-company transfers obfuscating provenance of illicit funds." } },
      { data: { id: "e15", source: "P002", target: "VEH001", rel_type: "DISPATCHED", rel_label: "Dispatched Van", weight: 3, color: "#ff2a55", doc: "fir_sandstorm_1.txt", metric: "Vehicle Escort", reason: "Kabir Sheikh coordinated driver itinerary for seized van." } },
      { data: { id: "e16", source: "VEH001", target: "LOC001", rel_type: "TRACKED_AT", rel_label: "GPS Port Tracking", weight: 3, color: "#00f0ff", doc: "fir_sandstorm_2.txt", metric: "GPS Geo-fence", reason: "Vehicle telematics show entry into Nhava Sheva CFS container dock." } },
      { data: { id: "e17", source: "ORG002", target: "LOC001", rel_type: "CONSIGNEE_AT", rel_label: "Customs Manifest", weight: 2, color: "#94a3b8", doc: "fir_sandstorm_2.txt", metric: "Bill of Lading", reason: "Freight handler listed on customs clearing documentation." } },

      // === Dense Candidate Background & Noise Edges (Non-syndicate baseline) ===
      { data: { id: "ne1", source: "P001", target: "N06", rel_type: "FAMILY_CALL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Routine Call", reason: "Personal conversation with parent; No syndicate content." } },
      { data: { id: "ne2", source: "P001", target: "N08", rel_type: "FAMILY_CALL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Routine Call", reason: "Personal family communication." } },
      { data: { id: "ne3", source: "P001", target: "N03", rel_type: "UPI_PAY", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Grocery ₹450", reason: "Retail store payment." } },
      { data: { id: "ne4", source: "P001", target: "N10", rel_type: "CARD_PAY", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Fuel ₹2,500", reason: "Gasoline station retail charge." } },
      { data: { id: "ne5", source: "P001", target: "N13", rel_type: "UTILITY_BILL", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Power ₹4,200", reason: "Household electricity payment." } },
      { data: { id: "ne6", source: "P002", target: "N01", rel_type: "CASUAL_CALL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Single Call", reason: "Brief daytime misdial; Zero repeated pattern." } },
      { data: { id: "ne7", source: "P002", target: "N09", rel_type: "FOOD_ORDER", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Meal ₹620", reason: "Food delivery payment." } },
      { data: { id: "ne8", source: "P002", target: "N12", rel_type: "CAB_FARE", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Transit ₹340", reason: "Ride-hailing service trip." } },
      { data: { id: "ne9", source: "P003", target: "N14", rel_type: "DOMESTIC_CALL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Spousal Call", reason: "Routine domestic check-in call." } },
      { data: { id: "ne10", source: "P003", target: "N11", rel_type: "POS_CHARGE", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Pharmacy ₹890", reason: "Medicine purchase." } },
      { data: { id: "ne11", source: "P004", target: "N04", rel_type: "PURCHASE", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Supplies ₹1,200", reason: "Retail shop stationery inventory." } },
      { data: { id: "ne12", source: "P004", target: "N07", rel_type: "MERCHANT_SETTLE", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Settlement", reason: "Commercial telecom top-up vendor settlement." } },
      { data: { id: "ne13", source: "P005", target: "N15", rel_type: "CONSULTATION", weight: 1.2, color: "#475569", doc: "fir_sandstorm_3.txt", metric: "Tax Audit", reason: "Legitimate corporate accounting audit review." } },
      { data: { id: "ne14", source: "W001", target: "N16", rel_type: "TOWER_TRANSIT", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Commute", reason: "Civilian witness commuting along highway." } },
      { data: { id: "ne15", source: "N01", target: "N17", rel_type: "TOWER_PING", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Andheri Ping", reason: "Independent suburban cellular activity." } },
      { data: { id: "ne16", source: "N02", target: "N20", rel_type: "COURIER_DISPATCH", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Delivery Alert", reason: "Commercial courier delivery notification." } },
      { data: { id: "ne17", source: "N05", target: "N17", rel_type: "CELL_CONNECTION", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Tower Andheri", reason: "Civilian user on Andheri cellular network." } },
      { data: { id: "ne18", source: "N20", target: "N21", rel_type: "MEAL_PAY", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "UPI ₹180", reason: "Canteen lunch transaction." } },
      { data: { id: "ne19", source: "N22", target: "TOW001", rel_type: "DUTY_LOG", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Guard Tower", reason: "Building security guard handset logged at tower." } },
      { data: { id: "ne20", source: "N06", target: "N23", rel_type: "PENSION_DEPOSIT", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Pension ₹32,000", reason: "Legitimate monthly pension credit." } },
      { data: { id: "ne21", source: "N08", target: "N24", rel_type: "SAVINGS_DEP", weight: 1.2, color: "#475569", doc: "txn_sandstorm.csv", metric: "Deposit ₹5,000", reason: "Routine bank savings transfer." } },
      { data: { id: "ne22", source: "N18", target: "PH001", rel_type: "BANK_SMS", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Automated SMS", reason: "Automated bank balance alert notification." } },
      { data: { id: "ne23", source: "N19", target: "PH002", rel_type: "SPAM_CALL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Robocall", reason: "Unsolicited promotional telemarketing call." } },
      { data: { id: "ne24", source: "LOC001", target: "TOW003", rel_type: "PORT_GEO", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Tower Area", reason: "Port geographic cell radius." } },
      { data: { id: "ne25", source: "TOW002", target: "TOW001", rel_type: "BACKHAUL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Telecom Grid", reason: "Standard municipal telecom backhaul connection." } },
      { data: { id: "ne26", source: "N25", target: "TOW001", rel_type: "ADJACENT_CELL", weight: 1.2, color: "#475569", doc: "cdr_sandstorm.csv", metric: "Neighbor Ping", reason: "Suburban railway cellular handoff." } }
    ];
  } else if (caseId === "phantom") {
    return [
      // === Core Extortion & Hawala Bridge Syndicate (Human Accused) ===
      { data: { id: "Q001", label: "Vikram Sinha", icon: "🚨", size: 38, type: "target", doc: "fir_phantom_1.txt", metric: "Cluster A Leader", reason: "Coordinated extortion intimidation from Delta Finance." } },
      { data: { id: "Q002", label: "Ravi Kumar", icon: "🚨", size: 30, type: "target", doc: "fir_phantom_1.txt", metric: "Enforcer Agent", reason: "Field intimidation operative threatening complainant." } },
      { data: { id: "Q003", label: "Neha Sharma", icon: "🟣", size: 26, type: "broker", doc: "fir_phantom_1.txt", metric: "Call Desk Operative", reason: "Routed coercive debt collection calls over VoIP trunks." } },
      { data: { id: "Q006", label: "Anand Krishnan", icon: "🟣", size: 40, type: "broker", doc: "fir_phantom_4.txt", metric: "Hidden Bridge (Low CC)", reason: "Sole intermediary linking Extortion Cluster A to Laundering Cluster B." } },
      { data: { id: "Q007", label: "Rohit Jain", icon: "🚨", size: 34, type: "target", doc: "fir_phantom_2.txt", metric: "Cluster B Receiver", reason: "Received layered extortion proceeds forwarded from Anand Krishnan." } },
      { data: { id: "Q008", label: "Amitabh Shah", icon: "🚨", size: 28, type: "target", doc: "fir_phantom_2.txt", metric: "Bullion Cashier", reason: "Converted hawala proceeds into unbilled physical bullion." } },
      
      // === Corporate Entities, Accounts & Handsets ===
      { data: { id: "ORG003", label: "Delta Finance Ltd", icon: "🏢", size: 34, type: "organization", doc: "fir_phantom_1.txt", metric: "Extortion Front", reason: "Front agency issuing coercive loan recovery threats." } },
      { data: { id: "ORG004", label: "Zenith Advisory LLP", icon: "🏢", size: 30, type: "organization", doc: "fir_phantom_4.txt", metric: "Conduit Entity", reason: "Consulting firm invoicing fake advisory charges to launder money." } },
      { data: { id: "ORG005", label: "Jain Bullion Traders", icon: "🏢", size: 32, type: "organization", doc: "fir_phantom_2.txt", metric: "Off-ramp Front", reason: "Gold merchant receiving multiple structured tranches." } },
      { data: { id: "ACC_DELTA", label: "HDFC-DELTA-8810", icon: "💳", size: 24, type: "account", doc: "txn_phantom.csv", metric: "Inflow Account", reason: "Account collecting coercive extortion payments." } },
      { data: { id: "ACC_ZENITH", label: "ICICI-ZEN-5501", icon: "💳", size: 24, type: "account", doc: "txn_phantom.csv", metric: "Transit Account", reason: "Bridge account distributing funds across Hawala conduits." } },
      { data: { id: "ACC_ROHIT", label: "SBI-JAIN-1092", icon: "💳", size: 24, type: "account", doc: "txn_phantom.csv", metric: "Off-ramp Account", reason: "Terminal account converting cash to bullion purchases." } },
      { data: { id: "PH_Q01", label: "+91-97300-11111", icon: "📱", size: 22, type: "phone", doc: "cdr_phantom.csv", metric: "Threat Calls", reason: "Cellular line issuing coercive extortion ultimatums." } },
      { data: { id: "PH_Q02", label: "+91-97300-22222", icon: "📱", size: 20, type: "phone", doc: "cdr_phantom.csv", metric: "VoIP Gateway", reason: "VoIP gateway SIM card masking extortion origin." } },
      { data: { id: "W002", label: "Lakshmi Devi", icon: "🟢", size: 24, type: "cleared", doc: "fir_phantom_1.txt", metric: "Victim / Complainant", reason: "Extortion victim who lodged FIR #0198." } },
      { data: { id: "W003", label: "Mohan Lal", icon: "🟢", size: 22, type: "cleared", doc: "fir_phantom_1.txt", metric: "Witness (Cleared)", reason: "Commercial property owner who witnessed extortion confrontation." } },

      // === Candidate Noise & Ambient Records (Simulating Thousands of Events) ===
      { data: { id: "N11", label: "97300-XXXX8", icon: "📱", size: 14, type: "noise", doc: "cdr_phantom.csv", metric: "Casual Call", reason: "Misdirected incoming inquiry; Cleared." } },
      { data: { id: "N12", label: "Suburban Medical", icon: "🏥", size: 15, type: "noise", doc: "txn_phantom.csv", metric: "Vendor UPI ₹820", reason: "Retail medical purchase; Cleared." } },
      { data: { id: "N13", label: "Gold Star Jewel", icon: "🪙", size: 15, type: "noise", doc: "txn_phantom.csv", metric: "Retail Purchase", reason: "Civilian festive ornament payment." } },
      { data: { id: "N14", label: "Delta IT Sol", icon: "🏢", size: 15, type: "noise", doc: "fir_phantom_1.txt", metric: "Unrelated Firm", reason: "Independent software firm sharing building floor." } },
      { data: { id: "N15", label: "Tower Nariman-01", icon: "📡", size: 18, type: "noise", doc: "cdr_phantom.csv", metric: "Financial District", reason: "Heavy business district traffic." } },
      { data: { id: "N16", label: "Tower Zaveri-03", icon: "📡", size: 18, type: "noise", doc: "cdr_phantom.csv", metric: "Bullion Market", reason: "Gold market cellular repeater." } },
      { data: { id: "N17", label: "Kishore CA", icon: "💼", size: 16, type: "noise", doc: "fir_phantom_4.txt", metric: "Auditor", reason: "Tax accounting firm filing GST returns." } },
      { data: { id: "N18", label: "Café Coffee Day", icon: "☕", size: 14, type: "noise", doc: "txn_phantom.csv", metric: "UPI ₹350", reason: "Meeting refreshments invoice." } },
      { data: { id: "N19", label: "DHL Express", icon: "📦", size: 15, type: "noise", doc: "cdr_phantom.csv", metric: "Package Delivery", reason: "Office correspondence tracking." } },
      { data: { id: "N20", label: "Pooja Loan", icon: "👤", size: 15, type: "noise", doc: "fir_phantom_1.txt", metric: "Civilian Applicant", reason: "Legitimate personal loan applicant rejected by Delta." } },
      { data: { id: "N21", label: "Tower Fort-C", icon: "📡", size: 18, type: "noise", doc: "cdr_phantom.csv", metric: "Suburban Tower", reason: "Suburban daytime phone traffic." } },
      { data: { id: "N22", label: "Post Office", icon: "🏢", size: 14, type: "noise", doc: "txn_phantom.csv", metric: "Stamp Duty ₹500", reason: "Court document stamp duty." } },
      { data: { id: "N23", label: "Airtel Broadband", icon: "⚡", size: 15, type: "noise", doc: "txn_phantom.csv", metric: "Internet ₹2,800", reason: "Monthly commercial broadband auto-debit." } },
      { data: { id: "N24", label: "Sunil Jain", icon: "👤", size: 16, type: "noise", doc: "cdr_phantom.csv", metric: "Family Contact", reason: "Rohit Jain's cousin residing in Surat." } },
      { data: { id: "N25", label: "97300-XXXX9", icon: "📱", size: 14, type: "noise", doc: "cdr_phantom.csv", metric: "Wrong Number", reason: "One-off incoming telemarketing ping." } },

      // === Verified Criminal Syndicate Edges ===
      { data: { id: "e10", source: "Q001", target: "ORG003", rel_type: "CONTROLS", rel_label: "Directs Front Firm", weight: 4, color: "#ff2a55", doc: "fir_phantom_1.txt", metric: "Executive", reason: "Directs operational extortion activities." } },
      { data: { id: "e11", source: "ORG003", target: "ACC_DELTA", rel_type: "BANK_ACCOUNT", rel_label: "Extortion Inflow", weight: 3, color: "#ff2a55", doc: "txn_phantom.csv", metric: "Collection Account", reason: "Primary bank account receiving coercive remittances." } },
      { data: { id: "e12", source: "Q001", target: "Q002", rel_type: "SUPERVISES", rel_label: "Field Enforcer", weight: 3, color: "#ff2a55", doc: "fir_phantom_1.txt", metric: "Direct Enforcer", reason: "Dispatched Ravi Kumar to conduct on-site physical intimidation." } },
      { data: { id: "e13", source: "Q001", target: "PH_Q01", rel_type: "ISSUES_THREATS", rel_label: "Extortion Calls", weight: 3.5, color: "#ff2a55", doc: "cdr_phantom.csv", metric: "Threat Calls", reason: "Coordinated intimidation calls from +91-97300-11111 citing Delta Finance." } },
      { data: { id: "e14", source: "ACC_DELTA", target: "ORG004", rel_type: "INVOICES_ADVISORY", rel_label: "Layering Invoices", weight: 3.5, color: "#ff2a55", doc: "txn_phantom.csv", metric: "Fake Invoices", reason: "Invoiced fake consulting charges to launder money." } },
      { data: { id: "e15", source: "ORG004", target: "Q006", rel_type: "HAWALA_BRIDGE", rel_label: "Cross-Cluster Bridge", weight: 4.5, color: "#a855f7", doc: "fir_phantom_4.txt", metric: "Structural Broker", reason: "ANO-004: Anand Krishnan acts as sole bridge linking extortion and laundering clusters." } },
      { data: { id: "e16", source: "Q006", target: "ACC_ZENITH", rel_type: "ROUTER_ACCOUNT", rel_label: "Transit Account", weight: 3.5, color: "#a855f7", doc: "txn_phantom.csv", metric: "Layering Router", reason: "Bridge account distributing funds across Hawala conduits." } },
      { data: { id: "e17", source: "ACC_ZENITH", target: "ACC_ROHIT", rel_type: "HAWALA_TRANCHE", rel_label: "6x Round Tranches", weight: 4.5, color: "#ff2a55", doc: "txn_phantom.csv", metric: "6x ₹15L Transfers", reason: "ANO-005: 6 transfers of exact amounts (₹5,00,000 & ₹10,00,000) routed to Rohit Jain." } },
      { data: { id: "e18", source: "Q006", target: "Q007", rel_type: "HAWALA_LINK", rel_label: "Hawala Remittance", weight: 4, color: "#a855f7", doc: "fir_phantom_2.txt", metric: "Direct Recipient", reason: "Forwarded extorted funds to Rohit Jain within 90 minutes of collection." } },
      { data: { id: "e19", source: "Q007", target: "ORG005", rel_type: "CONTROLS_ENTITY", rel_label: "Bullion Merchant", weight: 3.5, color: "#ff2a55", doc: "fir_phantom_2.txt", metric: "Sole Proprietor", reason: "Controls Jain Bullion Traders off-ramp." } },
      { data: { id: "e20", source: "ACC_ROHIT", target: "ORG005", rel_type: "BULLION_PURCHASE", rel_label: "2.8kg Gold Off-Ramp", weight: 4, color: "#ff2a55", doc: "txn_phantom.csv", metric: "Gold Off-Ramp", reason: "Converted illicit funds into 2.8 kg untraced gold bars." } },
      { data: { id: "e21", source: "Q007", target: "Q008", rel_type: "BULLION_CONSIGNMENT", rel_label: "Bullion Delivery", weight: 3, color: "#ff2a55", doc: "fir_phantom_2.txt", metric: "Cashier Pickup", reason: "Amitabh Shah executed physical bullion pickup." } },

      // === Noise & Ambient Connections ===
      { data: { id: "nqe1", source: "W002", target: "W003", rel_type: "NEIGHBOR_TALK", weight: 1.2, color: "#475569", doc: "fir_phantom_1.txt", metric: "Eyewitness Chat", reason: "Discussed extortion threat with shop neighbor." } },
      { data: { id: "nqe2", source: "Q001", target: "N14", rel_type: "SHARED_BUILDING", weight: 1.2, color: "#475569", doc: "fir_phantom_1.txt", metric: "Commercial Floor", reason: "Same commercial building tenant." } },
      { data: { id: "nqe3", source: "Q001", target: "N18", rel_type: "FOOD_UPI", weight: 1.2, color: "#475569", doc: "txn_phantom.csv", metric: "Coffee ₹350", reason: "Beverage retail bill." } },
      { data: { id: "nqe4", source: "Q002", target: "N12", rel_type: "MEDICAL_BUY", weight: 1.2, color: "#475569", doc: "txn_phantom.csv", metric: "Pharmacy ₹820", reason: "Personal medical purchase." } },
      { data: { id: "nqe5", source: "Q003", target: "N11", rel_type: "MISDIAL", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "1 Call", reason: "Accidental outbound misdial." } },
      { data: { id: "nqe6", source: "Q006", target: "N17", rel_type: "AUDIT_FILING", weight: 1.2, color: "#475569", doc: "fir_phantom_4.txt", metric: "Tax Retainer", reason: "Annual compliance accounting work." } },
      { data: { id: "nqe7", source: "Q006", target: "N19", rel_type: "COURIER", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "Mail Tracking", reason: "Document shipping service." } },
      { data: { id: "nqe8", source: "Q007", target: "N13", rel_type: "MARKET_INQUIRY", weight: 1.2, color: "#475569", doc: "txn_phantom.csv", metric: "Trade Rate", reason: "Inquiry on daily gold spot price." } },
      { data: { id: "nqe9", source: "Q007", target: "N24", rel_type: "FAMILY_CALL", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "Family Talk", reason: "Domestic phone call with relative." } },
      { data: { id: "nqe10", source: "ORG003", target: "N20", rel_type: "LOAN_APPLICATION", weight: 1.2, color: "#475569", doc: "fir_phantom_1.txt", metric: "Civilian Loan", reason: "Standard commercial loan application file." } },
      { data: { id: "nqe11", source: "ORG003", target: "N23", rel_type: "OFFICE_EXPENSE", weight: 1.2, color: "#475569", doc: "txn_phantom.csv", metric: "ISP ₹2,800", reason: "Telecom internet service invoice." } },
      { data: { id: "nqe12", source: "Q001", target: "N15", rel_type: "TOWER_TRAFFIC", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "Nariman Ping", reason: "Financial district cellular activity." } },
      { data: { id: "nqe13", source: "Q007", target: "N16", rel_type: "TOWER_TRAFFIC", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "Zaveri Ping", reason: "Gold market cellular registration." } },
      { data: { id: "nqe14", source: "W002", target: "N21", rel_type: "COMMUTE_TOWER", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "Suburban Ping", reason: "Victim residence cell tower." } },
      { data: { id: "nqe15", source: "ORG004", target: "N22", rel_type: "POSTAL_FEE", weight: 1.2, color: "#475569", doc: "txn_phantom.csv", metric: "Stamps ₹500", reason: "Postage fees for legal letters." } },
      { data: { id: "nqe16", source: "Q002", target: "N25", rel_type: "INBOUND_SPAM", weight: 1.2, color: "#475569", doc: "cdr_phantom.csv", metric: "Telemarketer", reason: "Unsolicited real estate marketing." } }
    ];
  } else {
    // === Case: Mirage (Night-Time SIM Swap & Mule Ring) ===
    return [
      // === Core Cyber-Fraud & SIM Swap Ring (Human Accused) ===
      { data: { id: "M001", label: "Imran Khan", icon: "🚨", size: 38, type: "target", doc: "fir_mirage_1.txt", metric: "Mule Account Holder", reason: "Received fraudulent OTP-authenticated transactions of ₹9,00,000 during SIM clone window." } },
      { data: { id: "M002", label: "Prakash Desai", icon: "🚨", size: 34, type: "target", doc: "fir_mirage_2.txt", metric: "Telecom Insider", reason: "Facilitated unauthorized SIM swap without verifying identity credentials." } },
      { data: { id: "M003", label: "Sunil Patil", icon: "🚨", size: 30, type: "target", doc: "fir_mirage_3.txt", metric: "Mule Recruiter", reason: "Recruited college student mule accounts to receive fragmented transfers." } },
      { data: { id: "M004", label: "Tariq Sheikh", icon: "🟣", size: 28, type: "broker", doc: "fir_mirage_1.txt", metric: "Dark Web Broker", reason: "Acquired leaked bank login credentials & victim Aadhaar details from telegram broker." } },
      { data: { id: "VIC001", label: "Alok Tandon", icon: "🟢", size: 26, type: "cleared", doc: "fir_mirage_1.txt", metric: "Victim (Account Owner)", reason: "Defrauded corporate executive whose mobile SIM was illegally ported." } },
      { data: { id: "PH_VIC", label: "+91-96200-55555", icon: "📱", size: 22, type: "phone", doc: "cdr_mirage.csv", metric: "Cloned MSISDN", reason: "Victim mobile number cloned during nocturnal hours to capture OTPs." } },
      { data: { id: "TOW001", label: "Tower BKC-112", icon: "📡", size: 28, type: "tower", doc: "cdr_mirage.csv", metric: "Spatial Co-Location", reason: "Tower pinged concurrently by 4 suspect SIMs immediately before night-time fraud execution." } },
      { data: { id: "TOW004", label: "Tower Kurla-W", icon: "📡", size: 22, type: "tower", doc: "cdr_mirage.csv", metric: "ATM Area Tower", reason: "Cell tower pinged during cash extraction at 03:15 AM." } },
      { data: { id: "STORE_01", label: "Franchise SIM Hub", icon: "🏢", size: 26, type: "organization", doc: "fir_mirage_2.txt", metric: "Point-of-Sale", reason: "Telecom franchise counter where duplicate SIM was issued unlawfully." } },
      { data: { id: "ACC_M01", label: "PNB-MULE-3301", icon: "💳", size: 24, type: "account", doc: "txn_mirage.csv", metric: "Primary Mule Acct", reason: "Received ₹4,50,000 transferred from victim net-banking at 02:14 AM." } },
      { data: { id: "ACC_M02", label: "BOB-MULE-8840", icon: "💳", size: 24, type: "account", doc: "txn_mirage.csv", metric: "Secondary Mule Acct", reason: "Received ₹4,50,000 structured tranche at 02:35 AM." } },
      { data: { id: "ATM_01", label: "ATM BKC Terminal", icon: "📍", size: 22, type: "location", doc: "txn_mirage.csv", metric: "Cash Extraction", reason: "Physical ATM kiosk where ₹1,50,000 cash was withdrawn at night." } },
      { data: { id: "ATM_02", label: "ATM Kurla Station", icon: "📍", size: 22, type: "location", doc: "txn_mirage.csv", metric: "Cash Extraction", reason: "Secondary ATM where ₹1,00,000 cash was withdrawn." } },
      { data: { id: "CRYPTO_01", label: "Binance P2P Mule", icon: "🪙", size: 26, type: "account", doc: "txn_mirage.csv", metric: "USDT Escrow", reason: "Remaining proceeds converted to USDT cryptocurrency." } },

      // === Dense Candidate Background Noise Field ===
      { data: { id: "N21", label: "96200-XXXX4", icon: "📱", size: 14, type: "noise", doc: "cdr_mirage.csv", metric: "Tower Signal Noise", reason: "Ordinary daytime caller on same tower; Cleared." } },
      { data: { id: "N22", label: "Kurla Hospital", icon: "🏥", size: 16, type: "noise", doc: "cdr_mirage.csv", metric: "Emergency Switchboard", reason: "Hospital telephone traffic; Zero criminal overlap." } },
      { data: { id: "N23", label: "Kamat Hotel", icon: "☕", size: 14, type: "noise", doc: "txn_mirage.csv", metric: "Tea Stall ₹40", reason: "Local night stall refreshment payment." } },
      { data: { id: "N24", label: "Bharat Petrol", icon: "🚗", size: 14, type: "noise", doc: "txn_mirage.csv", metric: "Civilian Withdrawal", reason: "Unrelated civilian cash withdrawal." } },
      { data: { id: "N25", label: "Tower Dadar-W", icon: "📡", size: 18, type: "noise", doc: "cdr_mirage.csv", metric: "Suburban Tower", reason: "Dadar residential area traffic." } },
      { data: { id: "N26", label: "Airtel IVR", icon: "📱", size: 15, type: "noise", doc: "cdr_mirage.csv", metric: "Automated Support", reason: "Victim's daytime service call reporting signal loss." } },
      { data: { id: "N27", label: "Rajan Store", icon: "🧾", size: 14, type: "noise", doc: "txn_mirage.csv", metric: "Grocery ₹290", reason: "Neighborhood convenience purchase." } },
      { data: { id: "N28", label: "96200-XXXX8", icon: "📱", size: 14, type: "noise", doc: "cdr_mirage.csv", metric: "Routine SMS", reason: "Daily promotional marketing dispatch." } },
      { data: { id: "N29", label: "Fastag Toll", icon: "🚗", size: 15, type: "noise", doc: "txn_mirage.csv", metric: "Toll ₹45", reason: "Toll plaza automated clearance." } },
      { data: { id: "N30", label: "Tower Vashi", icon: "📡", size: 18, type: "noise", doc: "cdr_mirage.csv", metric: "Bridge Tower", reason: "Highway vehicle movement logging." } },
      { data: { id: "N31", label: "Vandana Desai", icon: "👤", size: 16, type: "noise", doc: "fir_mirage_2.txt", metric: "Family Contact", reason: "Prakash Desai's spouse; Verified non-involved." } },
      { data: { id: "N32", label: "96200-XXXX9", icon: "📱", size: 14, type: "noise", doc: "cdr_mirage.csv", metric: "Missed Call", reason: "Civilian commuter misdirected call." } },

      // === Verified Criminal Edges ===
      { data: { id: "e20", source: "M002", target: "STORE_01", rel_type: "OPERATES_COUNTER", rel_label: "POS Franchise", weight: 3, color: "#ff2a55", doc: "fir_mirage_2.txt", metric: "Telecom Franchise", reason: "Prakash Desai managed POS terminal dispensing replacement SIM." } },
      { data: { id: "e21", source: "M002", target: "PH_VIC", rel_type: "FRAUDULENT_SWAP", rel_label: "Fraudulent SIM Clone", weight: 4.5, color: "#ff2a55", doc: "fir_mirage_2.txt", metric: "SIM Swap Action", reason: "Cloned victim number without biometric authentication." } },
      { data: { id: "e22", source: "M002", target: "TOW001", rel_type: "CO_LOCATED_AT", rel_label: "Tower Co-location", weight: 3.5, color: "#ff2a55", doc: "cdr_mirage.csv", metric: "29-Apr 22:30", reason: "ANO-007: Spatial graph co-occurrence during planning window." } },
      { data: { id: "e23", source: "M001", target: "TOW001", rel_type: "CO_LOCATED_AT", rel_label: "Tower Co-location", weight: 3.5, color: "#ff2a55", doc: "cdr_mirage.csv", metric: "29-Apr 22:30", reason: "ANO-007: Multiple suspect SIMs co-located at same cell tower." } },
      { data: { id: "e24", source: "M004", target: "M001", rel_type: "CREDENTIAL_LEAK", rel_label: "Dark Web Leaks", weight: 3.5, color: "#a855f7", doc: "fir_mirage_1.txt", metric: "Dark Web Lead", reason: "Transferred victim bank user ID and target phone data." } },
      { data: { id: "e25", source: "PH_VIC", target: "M001", rel_type: "OTP_FORWARD", rel_label: "Intercepted 2FA OTP", weight: 4.5, color: "#ffb800", doc: "cdr_mirage.csv", metric: "Intercepted OTP", reason: "Cloned SIM received net-banking OTPs at 02:13 AM." } },
      { data: { id: "e26", source: "M001", target: "ACC_M01", rel_type: "DRAIN_FUNDS", rel_label: "₹4.5L Mule Siphon 1", weight: 4.5, color: "#ff2a55", doc: "txn_mirage.csv", metric: "₹4,50,000 Transferred", reason: "ANO-006: Night-time high-velocity siphon to mule account 1." } },
      { data: { id: "e27", source: "M001", target: "ACC_M02", rel_type: "DRAIN_FUNDS", rel_label: "₹4.5L Mule Siphon 2", weight: 4.5, color: "#ff2a55", doc: "txn_mirage.csv", metric: "₹4,50,000 Transferred", reason: "ANO-006: Night-time siphon to mule account 2." } },
      { data: { id: "e28", source: "M003", target: "ACC_M01", rel_type: "CONTROLS_CARD", rel_label: "Mule ATM Card", weight: 3, color: "#ff2a55", doc: "fir_mirage_3.txt", metric: "Debit Card Mule", reason: "Possessed ATM debit card mapped to mule account 1." } },
      { data: { id: "e29", source: "M003", target: "ATM_01", rel_type: "CASH_WITHDRAWAL", rel_label: "₹1.5L ATM Withdrawal", weight: 4, color: "#ff2a55", doc: "txn_mirage.csv", metric: "₹1,50,000 Cash", reason: "Night ATM CCTV footage captures physical cash drain." } },
      { data: { id: "e30", source: "M003", target: "ATM_02", rel_type: "CASH_WITHDRAWAL", rel_label: "₹1.0L ATM Withdrawal", weight: 3.5, color: "#ff2a55", doc: "txn_mirage.csv", metric: "₹1,00,000 Cash", reason: "Second ATM cash extraction at Kurla station." } },
      { data: { id: "e31", source: "ACC_M02", target: "CRYPTO_01", rel_type: "P2P_PURCHASE", rel_label: "USDT Crypto Escrow", weight: 4, color: "#ff2a55", doc: "txn_mirage.csv", metric: "USDT Escrow", reason: "Converted ₹4,50,000 into offshore crypto stablecoins." } },
      { data: { id: "e32", source: "M003", target: "TOW004", rel_type: "TOWER_REGISTRATION", rel_label: "ATM Area Tower", weight: 2.5, color: "#ffb800", doc: "cdr_mirage.csv", metric: "03:15 AM Ping", reason: "Cellular ping co-occurring with Kurla ATM withdrawal." } },

      // === Noise & Ambient Edges ===
      { data: { id: "nme1", source: "VIC001", target: "N26", rel_type: "SUPPORT_CALL", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Helpline Log", reason: "Victim reported sudden cellular network cutoff." } },
      { data: { id: "nme2", source: "M002", target: "N31", rel_type: "SPOUSAL_CALL", weight: 1.2, color: "#475569", doc: "fir_mirage_2.txt", metric: "Home Call", reason: "Domestic telephone check-in." } },
      { data: { id: "nme3", source: "M003", target: "N23", rel_type: "TEA_PAY", weight: 1.2, color: "#475569", doc: "txn_mirage.csv", metric: "UPI ₹40", reason: "Late night tea stall purchase." } },
      { data: { id: "nme4", source: "N21", target: "TOW001", rel_type: "DAY_CALL", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Day Ping", reason: "Daytime cell tower connection." } },
      { data: { id: "nme5", source: "N24", target: "ATM_01", rel_type: "CIVILIAN_ATM", weight: 1.2, color: "#475569", doc: "txn_mirage.csv", metric: "ATM ₹2,000", reason: "Unrelated civilian cash withdrawal." } },
      { data: { id: "nme6", source: "N22", target: "TOW004", rel_type: "HOSPITAL_LINE", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Switchboard", reason: "Hospital trunk line registration." } },
      { data: { id: "nme7", source: "STORE_01", target: "N27", rel_type: "STORE_EXPENSE", weight: 1.2, color: "#475569", doc: "txn_mirage.csv", metric: "Retail ₹290", reason: "Franchise cleaning supply purchase." } },
      { data: { id: "nme8", source: "M001", target: "N25", rel_type: "DORMANT_TOWER", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Transit", reason: "Suburban travel between locations." } },
      { data: { id: "nme9", source: "N28", target: "PH_VIC", rel_type: "PROMO_SMS", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Marketing", reason: "Promotional telecom SMS." } },
      { data: { id: "nme10", source: "M003", target: "N29", rel_type: "TOLL_PAY", weight: 1.2, color: "#475569", doc: "txn_mirage.csv", metric: "Toll ₹45", reason: "Automated highway toll debit." } },
      { data: { id: "nme11", source: "N29", target: "N30", rel_type: "TOLL_GEO", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Bridge Tower", reason: "Vashi bridge cell registration." } },
      { data: { id: "nme12", source: "M002", target: "N32", rel_type: "MISSED_CALL", weight: 1.2, color: "#475569", doc: "cdr_mirage.csv", metric: "Wrong Ping", reason: "Single unanswered ring." } }
    ];
  }
};
