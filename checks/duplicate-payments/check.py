#!/usr/bin/env python3
"""Flag potential duplicate payments: same vendor, same/similar amount, close dates.

Usage: python check.py [path/to/ledger.csv]
Needs columns: invoice_no, invoice_date, vendor, amount
"""
import sys
from itertools import combinations
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
DAYS_WINDOW = 10        # how close two invoice dates must be to count as suspicious
AMOUNT_TOLERANCE = 0.0  # 0.0 = exact match; set to e.g. 1.0 to catch amounts within 1 kr
# ---------------------------

csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path, parse_dates=["invoice_date"])

findings = []
for vendor, grp in df.groupby("vendor"):
    rows = grp.sort_values("invoice_date").to_dict("records")
    for a, b in combinations(rows, 2):
        days = abs((b["invoice_date"] - a["invoice_date"]).days)
        if days <= DAYS_WINDOW and abs(a["amount"] - b["amount"]) <= AMOUNT_TOLERANCE:
            findings.append({
                "vendor": vendor, "amount": a["amount"],
                "invoice_1": a["invoice_no"], "date_1": a["invoice_date"].date(),
                "invoice_2": b["invoice_no"], "date_2": b["invoice_date"].date(),
                "days_apart": days,
            })

out = pd.DataFrame(findings)
print(f"=== Duplicate payment check: {len(out)} potential duplicate(s) ===")
if not out.empty:
    print(out.to_string(index=False))
    out.to_csv(Path(__file__).parent / "findings_duplicate_payments.csv", index=False)
    print(f"\nTotal exposure if all are true duplicates: {out['amount'].sum():,.2f}")
