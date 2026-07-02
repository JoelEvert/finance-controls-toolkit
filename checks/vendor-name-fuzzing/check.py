#!/usr/bin/env python3
"""Find near-duplicate vendor names — the root cause of duplicate payments and
fragmented spend reporting ("Nordic Supplies ApS" vs "Nordic Supplies APS").

Usage: python check.py [path/to/ledger.csv]
Needs columns: vendor, amount
"""
import sys
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
SIMILARITY_THRESHOLD = 0.85  # 1.0 = identical; lower = more aggressive matching
# ---------------------------


def normalize(name: str) -> str:
    n = name.lower()
    for suffix in [" aps", " a/s", " as", " ivs", " p/s", "&", ".", ","]:
        n = n.replace(suffix, " ")
    return " ".join(n.split())


csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path)

stats = df.groupby("vendor")["amount"].agg(["count", "sum"])
vendors = list(stats.index)

findings = []
for a, b in combinations(vendors, 2):
    ratio = SequenceMatcher(None, normalize(a), normalize(b)).ratio()
    if ratio >= SIMILARITY_THRESHOLD:
        findings.append({
            "vendor_1": a, "invoices_1": stats.loc[a, "count"], "spend_1": stats.loc[a, "sum"],
            "vendor_2": b, "invoices_2": stats.loc[b, "count"], "spend_2": stats.loc[b, "sum"],
            "similarity": round(ratio, 3),
        })

out = pd.DataFrame(findings).sort_values("similarity", ascending=False) if findings else pd.DataFrame()
print(f"=== Vendor name fuzzing: {len(out)} suspicious pair(s) ===")
if not out.empty:
    print(out.to_string(index=False))
    out.to_csv(Path(__file__).parent / "findings_vendor_names.csv", index=False)
