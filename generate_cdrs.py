"""
generate_cdrs.py
Generates synthetic CDR (Call Detail Record) CSVs for all 3 NEXUS cases.
Embeds designed anomalies per the anomaly ground truth table.

Schema:
  call_id, caller_msisdn, callee_msisdn, start_timestamp, duration_sec,
  call_type, caller_tower_id, caller_tower_lat, caller_tower_lon,
  callee_tower_id, callee_tower_lat, callee_tower_lon

Output:
  nexus/data/raw/cdrs/cdr_sandstorm.csv  (~4,000 rows)
  nexus/data/raw/cdrs/cdr_phantom.csv    (~3,500 rows)
  nexus/data/raw/cdrs/cdr_mirage.csv     (~3,800 rows)

Anomalies embedded:
  ANO-001: P001 (+91-98400-11111) makes 14 calls in 48h before 2025-03-15
  ANO-003: P001 contacts 4 new numbers within 24h on 2025-03-14
  ANO-007: R001–R004 + R002 all on Tower BKC-112, 29/04/2025 22:00–23:30

Run: python generate_cdrs.py
"""

import csv
import os
import random
import uuid
from datetime import datetime, timedelta

BASE = r"c:\Users\sudee\Desktop\SIH New\nexus\data\raw\cdrs"
os.makedirs(BASE, exist_ok=True)

FIELDNAMES = [
    "call_id", "caller_msisdn", "callee_msisdn", "start_timestamp",
    "duration_sec", "call_type",
    "caller_tower_id", "caller_tower_lat", "caller_tower_lon",
    "callee_tower_id", "callee_tower_lat", "callee_tower_lon"
]

rng = random.Random(42)


def uid():
    return str(uuid.uuid4())[:8].upper()


def ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:00")


def rand_dt(start: datetime, end: datetime,
            hour_min: int = 7, hour_max: int = 23) -> datetime:
    delta_days = (end - start).days
    day   = start + timedelta(days=rng.randint(0, max(0, delta_days)))
    hour  = rng.randint(hour_min, hour_max)
    mins  = rng.randint(0, 59)
    return day.replace(hour=hour, minute=mins, second=0, microsecond=0)


def rand_dur(short=False) -> int:
    """Duration in seconds. Short = SMS/brief calls."""
    if short:
        return rng.randint(5, 60)
    return rng.randint(15, 1800)


def noise_msisdn() -> str:
    prefixes = ["70420", "80720", "91761", "93400", "87890",
                "75300", "63990", "88200", "77540", "89120"]
    return f"+91-{rng.choice(prefixes)}-{rng.randint(10000, 99999)}"


def call_type() -> str:
    return rng.choice(["VOICE", "VOICE", "VOICE", "SMS"])


# ── Tower registries ────────────────────────────────────────────────────────
# (tower_id, lat, lon, area_name)
MUMBAI_TOWERS = [
    ("BOM-447", 19.0444, 72.8558, "Dharavi"),
    ("BOM-212", 19.0414, 72.8637, "Sion"),
    ("BOM-318", 19.1197, 72.8468, "Andheri W"),
    ("BOM-519", 19.0663, 72.8784, "Kurla"),
    ("BOM-621", 19.1360, 72.8296, "Malad W"),
    ("BOM-702", 19.0759, 72.8777, "Bandra E"),
    ("BOM-808", 19.0545, 72.9005, "Chembur"),
    ("BOM-901", 19.0296, 72.8553, "Dadar"),
    ("BOM-103", 18.9633, 72.8342, "Colaba"),
    ("BOM-244", 19.0990, 72.8490, "Santacruz"),
]
BKC_TOWER   = ("BKC-112", 19.0656, 72.8669, "BKC")
MLWD_TOWER  = ("MLW-088", 19.1870, 72.8411, "Malad W")

def rand_tower(towers=MUMBAI_TOWERS):
    t = rng.choice(towers)
    # Add tiny jitter (~50m) so coordinates aren't identical
    lat = t[1] + rng.uniform(-0.0005, 0.0005)
    lon = t[2] + rng.uniform(-0.0005, 0.0005)
    return t[0], round(lat, 6), round(lon, 6)


def make_call(caller, callee,
              dt_obj: datetime,
              caller_tower=None, callee_tower=None,
              ctype=None, dur=None) -> dict:
    ct = ctype or call_type()
    d  = dur   or rand_dur(short=(ct == "SMS"))
    c_tid, c_lat, c_lon = caller_tower or rand_tower()
    e_tid, e_lat, e_lon = callee_tower or rand_tower()
    return {
        "call_id":          uid(),
        "caller_msisdn":    caller,
        "callee_msisdn":    callee,
        "start_timestamp":  ts(dt_obj),
        "duration_sec":     d,
        "call_type":        ct,
        "caller_tower_id":  c_tid,
        "caller_tower_lat": c_lat,
        "caller_tower_lon": c_lon,
        "callee_tower_id":  e_tid,
        "callee_tower_lat": e_lat,
        "callee_tower_lon": e_lon,
    }


# ═══════════════════════════════════════════════════════════════════════════
# CASE 1 — OPERATION SANDSTORM
# ═══════════════════════════════════════════════════════════════════════════
# Phones:
#   P001: +91-98400-11111 (primary), +91-98400-12345 (burner)
#   P002: +91-98400-22222    P003: +91-98400-33333
#   P004: +91-98400-44444    P005: +91-98400-55555
#   Noise witness: +91-98400-77777
#
# Incident date: 2025-03-15 (seizure day)
# ANO-001: 14 calls from/to P001 in 48h window 2025-03-13 00:00 – 2025-03-14 23:59
# ANO-003: P001 contacts 4 NEW numbers within 24h on 2025-03-14
# ═══════════════════════════════════════════════════════════════════════════

sandstorm_rows = []
start_s  = datetime(2025,  1,  1)
end_s    = datetime(2025,  3, 12)   # baseline period
burst_s  = datetime(2025,  3, 13)   # burst window start
burst_e  = datetime(2025,  3, 14, 23, 59)
incident = datetime(2025,  3, 15)

PH_P001       = "+91-98400-11111"
PH_P001_BURN  = "+91-98400-12345"
PH_P002       = "+91-98400-22222"
PH_P003       = "+91-98400-33333"
PH_P004       = "+91-98400-44444"
PH_P005       = "+91-98400-55555"
PH_WITNESS    = "+91-98400-77777"

DHARAVI  = ("BOM-447", 19.0444, 72.8558)
SION_T   = ("BOM-212", 19.0414, 72.8637)
ANDHERI  = ("BOM-318", 19.1197, 72.8468)

# ── Baseline calls (normal frequency ~2 calls/day between suspect pairs) ──
network_pairs = [
    (PH_P001, PH_P002), (PH_P002, PH_P001),
    (PH_P001, PH_P003), (PH_P003, PH_P001),
    (PH_P002, PH_P003), (PH_P003, PH_P004),
    (PH_P004, PH_P005), (PH_P005, PH_P004),
    (PH_P001_BURN, PH_P002), (PH_P002, PH_P001_BURN),
]
for _ in range(180):
    caller, callee = rng.choice(network_pairs)
    sandstorm_rows.append(make_call(
        caller, callee,
        rand_dt(start_s, end_s),
        caller_tower=rand_tower([DHARAVI, SION_T])
    ))

# ── Innocent / noise calls (>20% of total) ──
for _ in range(2800):
    sandstorm_rows.append(make_call(
        noise_msisdn(), noise_msisdn(),
        rand_dt(start_s, incident)
    ))

# ── Witness calls (innocent) ──
for _ in range(30):
    sandstorm_rows.append(make_call(
        PH_WITNESS, noise_msisdn(),
        rand_dt(start_s, end_s)
    ))

# ── ANO-001: 14 calls in 48h burst window (2025-03-13 – 2025-03-14) ──────
burst_targets = [PH_P002, PH_P003, PH_P004, PH_P005,
                 PH_P001_BURN, PH_P002, PH_P003,
                 PH_P002, PH_P003, PH_P004, PH_P005,
                 PH_P002, PH_P003, PH_P002]  # 14 entries

for i, target in enumerate(burst_targets):
    hour = rng.randint(8, 23)
    day  = burst_s if i < 7 else burst_s + timedelta(days=1)
    dt   = day.replace(hour=hour, minute=rng.randint(0,59))
    sandstorm_rows.append(make_call(
        PH_P001, target, dt,
        caller_tower=DHARAVI,
        callee_tower=rand_tower([DHARAVI, SION_T, ANDHERI])
    ))

# ── ANO-003: P001 contacts 4 NEW numbers in 24h on 2025-03-14 ────────────
new_numbers = [noise_msisdn() for _ in range(4)]
for n in new_numbers:
    dt = burst_s.replace(hour=rng.randint(9,22),
                         minute=rng.randint(0,59)) + timedelta(days=1)
    sandstorm_rows.append(make_call(
        PH_P001, n, dt,
        caller_tower=DHARAVI
    ))

# ── Post-incident: burner phone goes silent (no calls after 15 Mar) ────────
for _ in range(5):
    sandstorm_rows.append(make_call(
        PH_P001_BURN, PH_P002,
        rand_dt(start_s, end_s),
        caller_tower=DHARAVI
    ))

rng.shuffle(sandstorm_rows)
print(f"Sandstorm CDR: {len(sandstorm_rows):,} rows")


# ═══════════════════════════════════════════════════════════════════════════
# CASE 2 — OPERATION PHANTOM
# ═══════════════════════════════════════════════════════════════════════════
# Phones:
#   Q001: +91-97300-11111  Q002: +91-97300-22222  Q003: +91-97300-33333
#   Q006: +91-97300-66666 (BRIDGE — calls both Cluster A and Cluster B)
#   Q007: +91-97300-77777  Victim: +91-97300-44444
#
# Key pattern: Q006 calls both Q001/Q002 (Cluster A) AND Q007 (Cluster B)
#              Without the CDR, there is no link between clusters
# ═══════════════════════════════════════════════════════════════════════════

phantom_rows = []
start_p = datetime(2025, 1, 15)
end_p   = datetime(2025, 4, 24)

QPH_Q001   = "+91-97300-11111"
QPH_Q002   = "+91-97300-22222"
QPH_Q003   = "+91-97300-33333"
QPH_VICTIM = "+91-97300-44444"
QPH_Q006   = "+91-97300-66666"   # ← BRIDGE
QPH_Q007   = "+91-97300-77777"

BKC_T  = (BKC_TOWER[0], BKC_TOWER[1], BKC_TOWER[2])
MALAD  = ("BOM-621", 19.1360, 72.8296)
BORIVALI = ("BOM-791", 19.2288, 72.8567)

# ── Cluster A internal calls ──
cluster_a_pairs = [
    (QPH_Q001, QPH_Q002), (QPH_Q002, QPH_Q001),
    (QPH_Q001, QPH_Q003), (QPH_Q003, QPH_Q001),
    (QPH_Q002, QPH_Q003),
]
for _ in range(200):
    caller, callee = rng.choice(cluster_a_pairs)
    phantom_rows.append(make_call(caller, callee, rand_dt(start_p, end_p)))

# ── Extortion calls from Q001 to victim ──
victim_harassment_dates = sorted([
    datetime(2025, 3, 1) + timedelta(days=rng.randint(0, 5)) for _ in range(8)
])
for dt in victim_harassment_dates:
    dt = dt.replace(hour=rng.randint(10, 20), minute=rng.randint(0, 59))
    phantom_rows.append(make_call(QPH_Q001, QPH_VICTIM, dt, dur=rng.randint(30, 180)))

# ── Q006 (BRIDGE) calls Cluster A ──────────────────────────────────────────
for _ in range(25):
    callee = rng.choice([QPH_Q001, QPH_Q002])
    phantom_rows.append(make_call(
        QPH_Q006, callee,
        rand_dt(start_p, end_p),
        caller_tower=BKC_T
    ))

# ── Q006 (BRIDGE) calls Cluster B ─ THE KEY CROSS-CLUSTER CDR ──────────────
for _ in range(18):
    phantom_rows.append(make_call(
        QPH_Q006, QPH_Q007,
        rand_dt(start_p, end_p),
        caller_tower=BKC_T
    ))

# ── Cluster B internal ──
for _ in range(80):
    phantom_rows.append(make_call(
        QPH_Q007, noise_msisdn(),
        rand_dt(start_p, end_p)
    ))

# ── Noise ──
for _ in range(3174):
    phantom_rows.append(make_call(
        noise_msisdn(), noise_msisdn(),
        rand_dt(start_p, end_p)
    ))

rng.shuffle(phantom_rows)
print(f"Phantom CDR:   {len(phantom_rows):,} rows")


# ═══════════════════════════════════════════════════════════════════════════
# CASE 3 — OPERATION MIRAGE
# ═══════════════════════════════════════════════════════════════════════════
# Phones:
#   R001: +91-96200-11111  R002: +91-96200-22222
#   R003: +91-96200-33333  R004: +91-96200-44444
#   Victims: +91-96200-55555 (Kavya), +91-96200-66666 (Thomas)
#
# ANO-007: R001, R002, R003, R004 ALL on Tower BKC-112 on 29/04/2025 22:00–23:30
#           AND on Tower MLW-088 on 08/05/2025 21:30–22:45
#           Physical co-location before each fraud wave
# ═══════════════════════════════════════════════════════════════════════════

mirage_rows = []
start_m = datetime(2025, 4, 15)
end_m   = datetime(2025, 5, 20)

RPH_R001   = "+91-96200-11111"
RPH_R002   = "+91-96200-22222"
RPH_R003   = "+91-96200-33333"
RPH_R004   = "+91-96200-44444"
RPH_KAVYA  = "+91-96200-55555"
RPH_THOMAS = "+91-96200-66666"

BKC_FIXED  = (BKC_TOWER[0], BKC_TOWER[1], BKC_TOWER[2])
MLW_FIXED  = (MLWD_TOWER[0], MLWD_TOWER[1], MLWD_TOWER[2])

# ── Ring coordination calls (R001 as hub) ──
ring_pairs = [
    (RPH_R001, RPH_R002), (RPH_R001, RPH_R003), (RPH_R001, RPH_R004),
    (RPH_R002, RPH_R001), (RPH_R003, RPH_R001), (RPH_R004, RPH_R001),
    (RPH_R002, RPH_R003), (RPH_R003, RPH_R004),
]
for _ in range(250):
    caller, callee = rng.choice(ring_pairs)
    mirage_rows.append(make_call(caller, callee, rand_dt(start_m, end_m)))

# ── ANO-007 Event 1: Co-location at BKC-112, 29/04/2025 22:00–23:30 ───────
coloc_1_base = datetime(2025, 4, 29, 22, 0)
suspects_phase1 = [RPH_R001, RPH_R002, RPH_R003, RPH_R004]
for i, phone in enumerate(suspects_phase1):
    # Each phone pings the same tower at slightly different minutes
    dt = coloc_1_base + timedelta(minutes=rng.randint(0, 90))
    # Short calls between ring members at the same location
    other = rng.choice([p for p in suspects_phase1 if p != phone])
    mirage_rows.append(make_call(
        phone, other, dt,
        caller_tower=BKC_FIXED,
        callee_tower=BKC_FIXED,
        ctype="VOICE", dur=rng.randint(20, 120)
    ))
# Extra tower registrations (phones idle on tower = SMS to noise)
for phone in suspects_phase1:
    for _ in range(3):
        dt = coloc_1_base + timedelta(minutes=rng.randint(5, 85))
        mirage_rows.append(make_call(
            phone, noise_msisdn(), dt,
            caller_tower=BKC_FIXED,
            ctype="SMS", dur=5
        ))

# ── ANO-007 Event 2: Co-location at MLW-088, 08/05/2025 21:30–22:45 ───────
coloc_2_base = datetime(2025, 5, 8, 21, 30)
for i, phone in enumerate(suspects_phase1):
    dt = coloc_2_base + timedelta(minutes=rng.randint(0, 75))
    other = rng.choice([p for p in suspects_phase1 if p != phone])
    mirage_rows.append(make_call(
        phone, other, dt,
        caller_tower=MLW_FIXED,
        callee_tower=MLW_FIXED,
        ctype="VOICE", dur=rng.randint(10, 90)
    ))
for phone in suspects_phase1:
    for _ in range(2):
        dt = coloc_2_base + timedelta(minutes=rng.randint(5, 70))
        mirage_rows.append(make_call(
            phone, noise_msisdn(), dt,
            caller_tower=MLW_FIXED,
            ctype="SMS", dur=5
        ))

# ── SIM-swap execution window: R002 calls victim numbers late night ─────────
for victim in [RPH_KAVYA, RPH_THOMAS]:
    # Calls just before SIM swap to confirm number is active
    pre_swap = datetime(2025, 4, 29, 21, rng.randint(0, 45))
    mirage_rows.append(make_call(
        RPH_R002, victim, pre_swap,
        caller_tower=BKC_FIXED,
        ctype="VOICE", dur=rng.randint(5, 20)
    ))

# ── R001 calls airport (before attempted departure) ──
for _ in range(3):
    dt = rand_dt(datetime(2025, 5, 17), datetime(2025, 5, 19))
    mirage_rows.append(make_call(RPH_R001, noise_msisdn(), dt))

# ── Noise ──
for _ in range(3463):
    mirage_rows.append(make_call(
        noise_msisdn(), noise_msisdn(),
        rand_dt(start_m, end_m)
    ))

rng.shuffle(mirage_rows)
print(f"Mirage CDR:    {len(mirage_rows):,} rows")


# ═══════════════════════════════════════════════════════════════════════════
# Write CSV files
# ═══════════════════════════════════════════════════════════════════════════

datasets = {
    "cdr_sandstorm.csv": sandstorm_rows,
    "cdr_phantom.csv":   phantom_rows,
    "cdr_mirage.csv":    mirage_rows,
}

for fname, rows in datasets.items():
    path = os.path.join(BASE, fname)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written: {fname}  ({len(rows):,} rows)")

print(f"\nDone. 3 CDR files written to {BASE}")


# ═══════════════════════════════════════════════════════════════════════════
# Anomaly Verification
# ═══════════════════════════════════════════════════════════════════════════
print("\n--- Anomaly Verification ---")

# ANO-001: P001 calls in 48h burst window
ano001 = [r for r in sandstorm_rows
          if r["caller_msisdn"] == PH_P001
          and "2025-03-13" <= r["start_timestamp"][:10] <= "2025-03-14"]
print(f"ANO-001  CDR burst (P001 in 48h): {len(ano001)} calls (expect 14+)")

# ANO-003: P001 contacts new numbers on 2025-03-14
known = {PH_P002, PH_P003, PH_P004, PH_P005, PH_P001_BURN}
ano003 = [r for r in sandstorm_rows
          if r["caller_msisdn"] == PH_P001
          and r["start_timestamp"][:10] == "2025-03-14"
          and r["callee_msisdn"] not in known]
print(f"ANO-003  New contacts on 14-Mar (P001): {len(ano003)} (expect 4)")

# Bridge: Q006 calls both clusters
bridge_a = [r for r in phantom_rows if r["caller_msisdn"] == QPH_Q006
            and r["callee_msisdn"] in (QPH_Q001, QPH_Q002)]
bridge_b = [r for r in phantom_rows if r["caller_msisdn"] == QPH_Q006
            and r["callee_msisdn"] == QPH_Q007]
print(f"Bridge   Q006->ClusterA: {len(bridge_a)} | Q006->ClusterB: {len(bridge_b)}")

# ANO-007: suspects on BKC-112 on 29 Apr
ano007 = [r for r in mirage_rows
          if r["caller_tower_id"] == "BKC-112"
          and r["start_timestamp"][:10] == "2025-04-29"
          and r["caller_msisdn"] in (RPH_R001, RPH_R002, RPH_R003, RPH_R004)]
print(f"ANO-007  Co-location at BKC-112 on 29-Apr: {len(ano007)} records (expect 16+)")

# Noise percentage check (sandstorm)
suspect_phones_s = {PH_P001, PH_P001_BURN, PH_P002, PH_P003, PH_P004, PH_P005, PH_WITNESS}
noise_calls_s = [r for r in sandstorm_rows if r["caller_msisdn"] not in suspect_phones_s]
print(f"Noise%%  Sandstorm: {100*len(noise_calls_s)/len(sandstorm_rows):.1f}%% noise (expect >20%%)")
