"""
generate_transactions.py
Generates synthetic transaction CSVs for all 3 NEXUS cases.
Embeds designed anomalies per the anomaly ground truth table.

Output:
  nexus/data/raw/transactions/txn_sandstorm.csv  (~600 rows)
  nexus/data/raw/transactions/txn_phantom.csv    (~500 rows)
  nexus/data/raw/transactions/txn_mirage.csv     (~600 rows)

Run: python generate_transactions.py
"""

import csv
import os
import random
import uuid
from datetime import datetime, timedelta

BASE = r"c:\Users\sudee\Desktop\SIH New\nexus\data\raw\transactions"
os.makedirs(BASE, exist_ok=True)

FIELDNAMES = [
    "txn_id", "sender_name", "sender_account", "sender_bank",
    "receiver_name", "receiver_account", "receiver_bank",
    "amount_inr", "timestamp", "txn_type", "reference_no", "remarks"
]

rng = random.Random(42)  # Fixed seed → reproducible


def uid():
    return str(uuid.uuid4())[:8].upper()


def rand_ts(start: datetime, end: datetime, hour_min=8, hour_max=20) -> str:
    """Random timestamp between start and end, constrained to business hours."""
    delta = (end - start).days
    day = start + timedelta(days=rng.randint(0, delta))
    hour = rng.randint(hour_min, hour_max)
    minute = rng.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=0).strftime("%Y-%m-%dT%H:%M:00")


def rand_ts_night(date: datetime) -> str:
    """Timestamp between 02:00 and 04:00 on a specific date (for fraud anomaly)."""
    hour = rng.randint(2, 3)
    minute = rng.randint(5, 55)
    return date.replace(hour=hour, minute=minute, second=0).strftime("%Y-%m-%dT%H:%M:00")


def txn_type():
    return rng.choice(["NEFT", "IMPS", "RTGS", "NEFT", "IMPS", "CASH"])


def noise_account():
    banks = ["SBI", "HDFC", "ICICI", "AXIS", "BOI", "PNB"]
    return f"{rng.choice(banks)}-XXXX-{rng.randint(1000,9999)}"


def noise_name():
    first = rng.choice([
        "Rajesh", "Anita", "Suresh", "Meena", "Vijay", "Rekha", "Anil",
        "Shobha", "Dinesh", "Lata", "Mahesh", "Priya", "Sanjay", "Usha"
    ])
    last = rng.choice([
        "Kumar", "Singh", "Patel", "Sharma", "Nair", "Menon", "Iyer",
        "Das", "Ghosh", "Roy", "Joshi", "Mishra", "Tiwari", "Pandey"
    ])
    return f"{first} {last}"


# ─────────────────────────────────────────────────────────────────────────────
# CASE 1 — OPERATION SANDSTORM (Narcotics / Structuring)
# Entities (aliases used, not canonical names):
#   P001=Arjun Mehta    → aliases: "A. Mehta", "Arjun Mehata"   ACC001=HDFC-XXXX-1001
#   P002=Deepak Rao     → aliases: "D. Rao", "Deepak R."         ACC003=SBI-XXXX-2001
#   P003=Sunita Verma   → aliases: "S. Verma", "Sunita V."       ACC004=SBI-XXXX-2002
#   ORG001=Phoenix Exports → "Phoenix Exports", "Phoenix Exp."   ACC002=HDFC-XXXX-1002
#   ORG002=Sunrise Traders → "Sunrise Trading Co."               ACC005=ICICI-XXXX-3001
#
# Anomalies:
#   ANO-002: 10 structuring txns ₹9.8L–₹9.95L  HDFC-XXXX-1001 → HDFC-XXXX-1002
#   Normal:  ~590 transactions mixing real+noise
# ─────────────────────────────────────────────────────────────────────────────

sandstorm_rows = []
start_s = datetime(2025, 1, 1)
end_s   = datetime(2025, 3, 13)

# Alias pools
p001_aliases = ["A. Mehta", "Arjun Mehata", "Arjun M."]
p002_aliases = ["D. Rao", "Deepak R.", "Deepak Rao"]
p003_aliases = ["S. Verma", "Sunita V.", "Sunitha Verma"]
org1_aliases = ["Phoenix Exports", "Phoenix Exp. Pvt Ltd", "Phoenix Exp."]
org2_aliases = ["Sunrise Trading Co.", "Sunrise Traders"]

# --- ANO-002: 10 structuring transactions (HDFC-XXXX-1001 → HDFC-XXXX-1002) ---
structuring_dates = sorted(rng.sample(range(5, 72), 10))  # spread over ~72 days
for i, day_offset in enumerate(structuring_dates):
    ts_date = start_s + timedelta(days=day_offset)
    amount  = rng.randint(9800000, 9950000)  # ₹9,80,000 – ₹9,95,000
    sandstorm_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(p001_aliases),
        "sender_account":   "HDFC-XXXX-1001",
        "sender_bank":      "HDFC",
        "receiver_name":    rng.choice(org1_aliases),
        "receiver_account": "HDFC-XXXX-1002",
        "receiver_bank":    "HDFC",
        "amount_inr":       amount,
        "timestamp":        rand_ts(ts_date, ts_date, 10, 16),
        "txn_type":         "NEFT",
        "reference_no":     f"HDFC{uid()}",
        "remarks":          "Commission payment – export services"
    })

# --- Shell company ORG001 → D. Rao (forward layering) ---
for _ in range(15):
    amount = rng.randint(200000, 900000)
    sandstorm_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(org1_aliases),
        "sender_account":   "HDFC-XXXX-1002",
        "sender_bank":      "HDFC",
        "receiver_name":    rng.choice(p002_aliases),
        "receiver_account": "SBI-XXXX-2001",
        "receiver_bank":    "SBI",
        "amount_inr":       amount,
        "timestamp":        rand_ts(start_s, end_s),
        "txn_type":         rng.choice(["NEFT", "IMPS"]),
        "reference_no":     f"SBI{uid()}",
        "remarks":          rng.choice(["Transport charges", "Logistics payment", "Delivery fee"])
    })

# --- D. Rao → Sunrise Traders (second shell) ---
for _ in range(12):
    amount = rng.randint(100000, 500000)
    sandstorm_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(p002_aliases),
        "sender_account":   "SBI-XXXX-2001",
        "sender_bank":      "SBI",
        "receiver_name":    rng.choice(org2_aliases),
        "receiver_account": "ICICI-XXXX-3001",
        "receiver_bank":    "ICICI",
        "amount_inr":       amount,
        "timestamp":        rand_ts(start_s, end_s),
        "txn_type":         "NEFT",
        "reference_no":     f"ICICI{uid()}",
        "remarks":          "Goods payment"
    })

# --- S. Verma → Sunrise Traders ---
for _ in range(10):
    amount = rng.randint(50000, 300000)
    sandstorm_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(p003_aliases),
        "sender_account":   "SBI-XXXX-2002",
        "sender_bank":      "SBI",
        "receiver_name":    rng.choice(org2_aliases),
        "receiver_account": "ICICI-XXXX-3001",
        "receiver_bank":    "ICICI",
        "amount_inr":       amount,
        "timestamp":        rand_ts(start_s, end_s),
        "txn_type":         rng.choice(["NEFT", "CASH"]),
        "reference_no":     f"ICICI{uid()}",
        "remarks":          "Accounts payable"
    })

# --- Noise transactions (innocent parties) ---
for _ in range(553):
    sname = noise_name()
    rname = noise_name()
    sandstorm_rows.append({
        "txn_id":           uid(),
        "sender_name":      sname,
        "sender_account":   noise_account(),
        "sender_bank":      rng.choice(["SBI", "HDFC", "ICICI", "AXIS", "BOI"]),
        "receiver_name":    rname,
        "receiver_account": noise_account(),
        "receiver_bank":    rng.choice(["SBI", "HDFC", "ICICI", "AXIS", "BOI"]),
        "amount_inr":       rng.randint(5000, 200000),
        "timestamp":        rand_ts(start_s, end_s),
        "txn_type":         txn_type(),
        "reference_no":     f"REF{uid()}",
        "remarks":          rng.choice(["Personal transfer", "Rent payment", "Salary", "Invoice payment", ""])
    })

rng.shuffle(sandstorm_rows)

# ─────────────────────────────────────────────────────────────────────────────
# CASE 2 — OPERATION PHANTOM (Extortion / Hawala)
# Entities:
#   Q001=Vikram Sinha   → "V. Sinha", "Vikram S."       BACC001=AXIS-XXXX-4001
#   Q002=Meera Nambiar  → "M. Nambiar", "Meera N."      BACC002=AXIS-XXXX-4002
#   Q006=Anand Krishnan → "A. Krishnan", "Aanand K."    BACC003=HDFC-XXXX-4003  ← BRIDGE
#   Q007=Rohit Jain     → "R. Jain", "Rohit J."         BACC004=SBI-XXXX-4004
#   Q008=Neha Gupta     → "N. Gupta"                    (no account, cash only)
#   ORG003=Delta Finance → "Delta Finance", "Delta Fin." BACC005=YES-XXXX-5001
#   ORG004=Sigma Holdings → "Sigma Hold."               BACC006=YES-XXXX-5002
#
# Anomalies:
#   ANO-005: 6 exact round-number transfers (₹5,00,000 / ₹10,00,000) → BACC002
#   BRIDGE:  BACC005 (Delta Finance) → BACC003 (A. Krishnan) → BACC004 (Rohit J.)
# ─────────────────────────────────────────────────────────────────────────────

phantom_rows = []
start_p = datetime(2025, 1, 15)
end_p   = datetime(2025, 4, 5)

q001_aliases = ["V. Sinha", "Vikram S.", "Vikram Sinha"]
q002_aliases = ["M. Nambiar", "Meera N.", "Meera Nambiar"]
q006_aliases = ["A. Krishnan", "Aanand Krishnan", "Anand K."]
q007_aliases = ["R. Jain", "Rohit J."]
org3_aliases = ["Delta Finance Ltd", "Delta Finance", "Delta Fin. Ltd"]
org4_aliases = ["Sigma Holdings", "Sigma Hold."]

# --- ANO-005: 6 exact round-number hawala transfers → BACC002 ---
hawala_amounts = [500000, 500000, 1000000, 500000, 1000000, 500000]
hawala_day_offsets = sorted(rng.sample(range(5, 75), 6))
for amount, day_offset in zip(hawala_amounts, hawala_day_offsets):
    ts_date = start_p + timedelta(days=day_offset)
    phantom_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(q001_aliases),
        "sender_account":   "AXIS-XXXX-4001",
        "sender_bank":      "AXIS",
        "receiver_name":    rng.choice(q002_aliases),
        "receiver_account": "AXIS-XXXX-4002",
        "receiver_bank":    "AXIS",
        "amount_inr":       amount,
        "timestamp":        rand_ts(ts_date, ts_date, 11, 17),
        "txn_type":         "RTGS",
        "reference_no":     f"AXIS{uid()}",
        "remarks":          "Business settlement"
    })

# --- BACC002 → Delta Finance (forward layering) ---
for i in range(6):
    day_offset = hawala_day_offsets[i] + rng.randint(1, 2)
    ts_date = start_p + timedelta(days=min(day_offset, 79))
    phantom_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(q002_aliases),
        "sender_account":   "AXIS-XXXX-4002",
        "sender_bank":      "AXIS",
        "receiver_name":    rng.choice(org3_aliases),
        "receiver_account": "YES-XXXX-5001",
        "receiver_bank":    "YES",
        "amount_inr":       hawala_amounts[i],
        "timestamp":        rand_ts(ts_date, ts_date, 9, 18),
        "txn_type":         "RTGS",
        "reference_no":     f"YES{uid()}",
        "remarks":          "Consulting fees"
    })

# --- BRIDGE: Delta Finance → A. Krishnan → Rohit J. ---
bridge_dates = [datetime(2025, 3, 15), datetime(2025, 4, 1)]
bridge_amounts = [1000000, 500000]
for bd, ba in zip(bridge_dates, bridge_amounts):
    # Leg 1: Delta Finance → A. Krishnan
    phantom_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(org3_aliases),
        "sender_account":   "YES-XXXX-5001",
        "sender_bank":      "YES",
        "receiver_name":    rng.choice(q006_aliases),
        "receiver_account": "HDFC-XXXX-4003",
        "receiver_bank":    "HDFC",
        "amount_inr":       ba,
        "timestamp":        bd.strftime("%Y-%m-%dT%H:%M:00").replace("T00:00", f"T{rng.randint(10,14):02d}:{rng.randint(0,59):02d}"),
        "txn_type":         "RTGS",
        "reference_no":     f"HDFC{uid()}",
        "remarks":          "Inter-company transfer"
    })
    # Leg 2: A. Krishnan → Rohit Jain (within 24h) — THE KEY BRIDGE TRANSACTION
    next_day = bd + timedelta(hours=rng.randint(6, 22))
    phantom_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(q006_aliases),
        "sender_account":   "HDFC-XXXX-4003",
        "sender_bank":      "HDFC",
        "receiver_name":    rng.choice(q007_aliases),
        "receiver_account": "SBI-XXXX-4004",
        "receiver_bank":    "SBI",
        "amount_inr":       ba,
        "timestamp":        next_day.strftime("%Y-%m-%dT%H:%M:00").replace("T00:", f"T{rng.randint(10,16):02d}:"),
        "txn_type":         "NEFT",
        "reference_no":     f"SBI{uid()}",
        "remarks":          "Settlement"
    })

# --- Cluster B internal (Rohit Jain / Sigma Holdings) ---
for _ in range(15):
    phantom_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(q007_aliases),
        "sender_account":   "SBI-XXXX-4004",
        "sender_bank":      "SBI",
        "receiver_name":    rng.choice(org4_aliases),
        "receiver_account": "YES-XXXX-5002",
        "receiver_bank":    "YES",
        "amount_inr":       rng.randint(100000, 800000),
        "timestamp":        rand_ts(start_p, end_p),
        "txn_type":         rng.choice(["NEFT", "IMPS"]),
        "reference_no":     f"YES{uid()}",
        "remarks":          "Service payment"
    })

# --- Noise transactions ---
for _ in range(461):
    phantom_rows.append({
        "txn_id":           uid(),
        "sender_name":      noise_name(),
        "sender_account":   noise_account(),
        "sender_bank":      rng.choice(["SBI", "HDFC", "ICICI", "AXIS", "BOI"]),
        "receiver_name":    noise_name(),
        "receiver_account": noise_account(),
        "receiver_bank":    rng.choice(["SBI", "HDFC", "ICICI", "AXIS", "BOI"]),
        "amount_inr":       rng.randint(5000, 500000),
        "timestamp":        rand_ts(start_p, end_p),
        "txn_type":         txn_type(),
        "reference_no":     f"REF{uid()}",
        "remarks":          rng.choice(["Personal", "Rent", "Invoice", "EMI", ""])
    })

rng.shuffle(phantom_rows)

# ─────────────────────────────────────────────────────────────────────────────
# CASE 3 — OPERATION MIRAGE (SIM-Swap / Identity Fraud)
# Entities:
#   R001=Imran Khan  → "I. Khan", "Imraan Khan"    CACC001=PNB-XXXX-6001
#   R002=Pooja Desai → "P. Desai", "Pooja D."      CACC002=PNB-XXXX-6002
#   R003=Arun Tiwari → "A. Tiwari", "Arun Tiwary"  CACC003=BOI-XXXX-6003
#   R004=Sanjay Yadav → "S. Yadav", "Sanjay Y."   CACC004=BOI-XXXX-6004
#   ORG005=Apex Digital Services → "Apex Digital Svcs" CACC005=KOTAK-XXXX-7001
#   ORG006=NextGen Solutions → "NextGen Sol."       CACC006=KOTAK-XXXX-7002
#
# Anomalies:
#   ANO-006: 8 transactions > ₹4,00,000 between 02:00–04:00 to new recipients
#            → IsolationForest flags on [amount, hour_of_day, is_new_recipient]
# ─────────────────────────────────────────────────────────────────────────────

mirage_rows = []
start_m = datetime(2025, 4, 15)
end_m   = datetime(2025, 5, 20)

r001_aliases = ["I. Khan", "Imraan Khan", "Imran K."]
r002_aliases = ["P. Desai", "Pooja D.", "Pooja Desai"]
r003_aliases = ["A. Tiwari", "Arun Tiwary"]
r004_aliases = ["S. Yadav", "Sanjay Y."]
org5_aliases = ["Apex Digital Svcs", "Apex Digital Services", "Apex Dig. Svcs"]
org6_aliases = ["NextGen Sol.", "NextGen Solutions"]

# Victim accounts (source of stolen funds)
victim_accounts = [
    ("Kavya Nair",    noise_account(), "CANARA"),
    ("Thomas Mathew", noise_account(), "CANARA"),
    ("R. Sharma",     noise_account(), "SBI"),
    ("Anand Mehta",   noise_account(), "HDFC"),
    ("S. Krishnan",   noise_account(), "ICICI"),
    ("P. Iyer",       noise_account(), "BOI"),
    ("Vijay Pillai",  noise_account(), "AXIS"),
    ("Meena Das",     noise_account(), "PNB"),
]

# --- ANO-006: 8 night-time high-value fraud transactions ---
fraud_dates_offsets = sorted(rng.sample(range(0, 35), 8))
fraud_receivers = [
    ("PNB-XXXX-6001",   "PNB",   r001_aliases),
    ("KOTAK-XXXX-7001", "KOTAK", org5_aliases),
    ("BOI-XXXX-6003",   "BOI",   r003_aliases),
    ("BOI-XXXX-6004",   "BOI",   r004_aliases),
    ("KOTAK-XXXX-7002", "KOTAK", org6_aliases),
    ("PNB-XXXX-6001",   "PNB",   r001_aliases),
    ("BOI-XXXX-6003",   "BOI",   r003_aliases),
    ("KOTAK-XXXX-7001", "KOTAK", org5_aliases),
]
for i, (day_offset, (recv_acc, recv_bank, recv_aliases)) in enumerate(
        zip(fraud_dates_offsets, fraud_receivers)):
    fraud_date = start_m + timedelta(days=day_offset)
    victim = victim_accounts[i]
    amount = rng.randint(4000000, 4800000)  # ₹4,00,000 – ₹4,80,000
    mirage_rows.append({
        "txn_id":           uid(),
        "sender_name":      victim[0],
        "sender_account":   victim[1],
        "sender_bank":      victim[2],
        "receiver_name":    rng.choice(recv_aliases),
        "receiver_account": recv_acc,
        "receiver_bank":    recv_bank,
        "amount_inr":       amount,
        "timestamp":        rand_ts_night(fraud_date),   # 02:00–04:00 ← anomalous
        "txn_type":         "IMPS",
        "reference_no":     f"IMPS{uid()}",
        "remarks":          "Online transfer"            # generic remark
    })

# --- Immediate onward transfer (within hours, money mule pattern) ---
mule_map = {
    "PNB-XXXX-6001":   ("BOI-XXXX-6003",   rng.choice(r003_aliases)),
    "KOTAK-XXXX-7001": ("BOI-XXXX-6004",   rng.choice(r004_aliases)),
    "BOI-XXXX-6003":   ("PNB-XXXX-6001",   rng.choice(r001_aliases)),
    "BOI-XXXX-6004":   ("KOTAK-XXXX-7001", rng.choice(org5_aliases)),
    "KOTAK-XXXX-7002": ("PNB-XXXX-6001",   rng.choice(r001_aliases)),
}
for fraud_row in mirage_rows[:8]:
    src_acc = fraud_row["receiver_account"]
    if src_acc in mule_map:
        dst_acc, dst_name = mule_map[src_acc]
        ts = datetime.strptime(fraud_row["timestamp"], "%Y-%m-%dT%H:%M:00")
        ts_onward = ts + timedelta(hours=rng.randint(1, 5))
        mirage_rows.append({
            "txn_id":           uid(),
            "sender_name":      fraud_row["receiver_name"],
            "sender_account":   src_acc,
            "sender_bank":      fraud_row["receiver_bank"],
            "receiver_name":    dst_name,
            "receiver_account": dst_acc,
            "receiver_bank":    rng.choice(["PNB", "BOI", "KOTAK"]),
            "amount_inr":       fraud_row["amount_inr"] - rng.randint(10000, 50000),
            "timestamp":        ts_onward.strftime("%Y-%m-%dT%H:%M:00"),
            "txn_type":         "IMPS",
            "reference_no":     f"IMPS{uid()}",
            "remarks":          ""
        })

# --- Normal daytime activity for suspects (cover transactions) ---
for _ in range(30):
    mirage_rows.append({
        "txn_id":           uid(),
        "sender_name":      rng.choice(r001_aliases + r003_aliases + r004_aliases),
        "sender_account":   rng.choice(["PNB-XXXX-6001", "BOI-XXXX-6003", "BOI-XXXX-6004"]),
        "sender_bank":      rng.choice(["PNB", "BOI"]),
        "receiver_name":    noise_name(),
        "receiver_account": noise_account(),
        "receiver_bank":    rng.choice(["SBI", "HDFC", "ICICI"]),
        "amount_inr":       rng.randint(5000, 30000),
        "timestamp":        rand_ts(start_m, end_m, 9, 18),
        "txn_type":         rng.choice(["NEFT", "IMPS", "UPI"]),
        "reference_no":     f"REF{uid()}",
        "remarks":          rng.choice(["Grocery", "Rent", "Recharge", ""])
    })

# --- Noise transactions ---
for _ in range(548):
    mirage_rows.append({
        "txn_id":           uid(),
        "sender_name":      noise_name(),
        "sender_account":   noise_account(),
        "sender_bank":      rng.choice(["SBI", "HDFC", "ICICI", "AXIS", "BOI"]),
        "receiver_name":    noise_name(),
        "receiver_account": noise_account(),
        "receiver_bank":    rng.choice(["SBI", "HDFC", "ICICI", "AXIS", "BOI"]),
        "amount_inr":       rng.randint(5000, 150000),
        "timestamp":        rand_ts(start_m, end_m, 8, 22),
        "txn_type":         txn_type(),
        "reference_no":     f"REF{uid()}",
        "remarks":          rng.choice(["Personal", "Invoice", "EMI", "Rent", ""])
    })

rng.shuffle(mirage_rows)

# ─────────────────────────────────────────────────────────────────────────────
# Write all CSVs
# ─────────────────────────────────────────────────────────────────────────────

datasets = {
    "txn_sandstorm.csv": sandstorm_rows,
    "txn_phantom.csv":   phantom_rows,
    "txn_mirage.csv":    mirage_rows,
}

for fname, rows in datasets.items():
    path = os.path.join(BASE, fname)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written: {fname}  ({len(rows):,} rows)")

print(f"\nDone. 3 transaction files written to {BASE}")

# ─── Quick anomaly verification ────────────────────────────────────────────
print("\n--- Anomaly Verification ---")

# ANO-002 check (sandstorm structuring)
ano002 = [r for r in sandstorm_rows
          if r["sender_account"] == "HDFC-XXXX-1001"
          and r["receiver_account"] == "HDFC-XXXX-1002"
          and int(r["amount_inr"]) >= 9800000]
print(f"ANO-002 Structuring txns: {len(ano002)} (expect 10)")

# ANO-005 check (phantom round-number)
ano005 = [r for r in phantom_rows
          if int(r["amount_inr"]) in (500000, 1000000)
          and r["receiver_account"] == "AXIS-XXXX-4002"]
print(f"ANO-005 Hawala round-number txns: {len(ano005)} (expect 6)")

# Bridge check (phantom)
bridge = [r for r in phantom_rows
          if r["sender_account"] == "HDFC-XXXX-4003"
          and r["receiver_account"] == "SBI-XXXX-4004"]
print(f"Bridge txns (Delta Fin → A.Krishnan → Rohit J.): {len(bridge)} (expect 2)")

# ANO-006 check (mirage night-time)
ano006 = [r for r in mirage_rows
          if int(r["amount_inr"]) >= 4000000
          and "T02:" in r["timestamp"] or "T03:" in r["timestamp"]]
print(f"ANO-006 Night-time high-value txns: ~{len(ano006)} (expect ~8)")
