#!/usr/bin/env python3
"""Flag vendors with suspiciously many round-number invoices. Genuine invoices
rarely land on 10,000.00 exactly; estimates, fabrications and lazy accruals do.

Usage: python check.py [path/to/ledger.csv]
Needs columns: invoice_no, invoice_date, vendor, amount
"""
import sys
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
ROUND_TO = 1000        # what counts as "round": divisible by this
MIN_ROUND_INVOICES = 3   # only report vendors with at least this many round invoices
MIN_ROUND_SHARE = 0.15   # ...and where round invoices are at least this share of their total
# ---------------------------

csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path)

df["is_round"] = (df["amount"] % ROUND_TO == 0) & (df["amount"] > 0)
summary = df.groupby("vendor").agg(
    total_invoices=("amount", "count"),
    round_invoices=("is_round", "sum"),
    round_spend=("amount", lambda s: s[df.loc[s.index, "is_round"]].sum()),
)
summary["round_share"] = (summary["round_invoices"] / summary["total_invoices"]).round(2)
flagged = summary[
    (summary["round_invoices"] >= MIN_ROUND_INVOICES)
    & (summary["round_share"] >= MIN_ROUND_SHARE)
].sort_values("round_share", ascending=False)

print(f"=== Round number check: {len(flagged)} vendor(s) flagged ===")
if not flagged.empty:
    print(flagged.to_string())
    detail = df[df["is_round"] & df["vendor"].isin(flagged.index)]
    detail[["invoice_no", "invoice_date", "vendor", "amount"]].to_csv(
        Path(__file__).parent / "findings_round_numbers.csv", index=False)
    print(f"\nDetail rows saved: {len(detail)}")
