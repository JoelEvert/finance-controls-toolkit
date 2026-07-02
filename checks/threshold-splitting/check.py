#!/usr/bin/env python3
"""Detect invoices clustered just under an approval threshold — the pattern left
behind when someone splits a purchase to dodge sign-off.

Usage: python check.py [path/to/ledger.csv]
Needs columns: invoice_no, invoice_date, vendor, amount, posted_by
"""
import sys
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
APPROVAL_LIMIT = 10000   # your approval threshold
UNDER_BAND = 0.05        # "just under" = within 5% below the limit
MIN_HITS = 3             # flag vendor/requester combos with at least this many
WINDOW_DAYS = 60         # ...within this many days
# ---------------------------

csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path, parse_dates=["invoice_date"])

lo = APPROVAL_LIMIT * (1 - UNDER_BAND)
near = df[(df["amount"] >= lo) & (df["amount"] < APPROVAL_LIMIT)].copy()

findings = []
for (vendor, who), grp in near.groupby(["vendor", "posted_by"]):
    grp = grp.sort_values("invoice_date")
    span = (grp["invoice_date"].max() - grp["invoice_date"].min()).days
    if len(grp) >= MIN_HITS and span <= WINDOW_DAYS:
        findings.append({
            "vendor": vendor, "posted_by": who, "invoices": len(grp),
            "days_span": span, "total": grp["amount"].sum(),
            "amounts": ", ".join(f"{a:,.0f}" for a in grp["amount"]),
        })

out = pd.DataFrame(findings)
print(f"=== Threshold splitting check (limit {APPROVAL_LIMIT:,}): {len(out)} pattern(s) ===")
if not out.empty:
    print(out.to_string(index=False))
    near[near.set_index(["vendor", "posted_by"]).index.isin(
        out.set_index(["vendor", "posted_by"]).index)][
        ["invoice_no", "invoice_date", "vendor", "amount", "posted_by"]
    ].to_csv(Path(__file__).parent / "findings_threshold_splitting.csv", index=False)
