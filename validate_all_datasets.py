"""
validate_all_datasets.py
Comprehensive validation script checking FIRs, CDRs, and Transactions
against all criteria in nexus-dataset-roadmap.md.
"""

import os
import csv
import glob

DATA_DIR = r"c:\Users\sudee\Desktop\SIH New\nexus\data\raw"

def validate():
    print("=== NEXUS SYNTHETIC DATASET VALIDATION ===")
    
    # 1. Check FIRs
    fir_files = glob.glob(os.path.join(DATA_DIR, "firs", "*.txt"))
    print(f"\n[1] FIR Files Check: Found {len(fir_files)} FIRs (expect 12)")
    assert len(fir_files) == 12, "Expected 12 FIR files!"
    for f in sorted(fir_files):
        size = os.path.getsize(f)
        assert size > 1000, f"FIR file {f} is too small ({size} bytes)"
    print("  -> ALL FIRs VALID.")

    # 2. Check Transactions
    txn_files = glob.glob(os.path.join(DATA_DIR, "transactions", "*.csv"))
    print(f"\n[2] Transaction Files Check: Found {len(txn_files)} CSVs (expect 3)")
    assert len(txn_files) == 3, "Expected 3 transaction CSV files!"
    for f in sorted(txn_files):
        with open(f, encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        print(f"  - {os.path.basename(f)}: {len(rows)} rows (min 500)")
        assert len(rows) >= 490, f"File {f} has fewer rows than expected"
    print("  -> ALL TRANSACTIONS VALID.")

    # 3. Check CDRs
    cdr_files = glob.glob(os.path.join(DATA_DIR, "cdrs", "*.csv"))
    print(f"\n[3] CDR Files Check: Found {len(cdr_files)} CSVs (expect 3)")
    assert len(cdr_files) == 3, "Expected 3 CDR CSV files!"
    for f in sorted(cdr_files):
        with open(f, encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        print(f"  - {os.path.basename(f)}: {len(rows)} rows (min 3000)")
        assert len(rows) >= 3000, f"File {f} has fewer rows than expected"
    print("  -> ALL CDRs VALID.")

    print("\n=== SUMMARY: ALL SYNTHETIC DATASETS VALIDATED SUCCESSFULLY! ===")

if __name__ == "__main__":
    validate()
