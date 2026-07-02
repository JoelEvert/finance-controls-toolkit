#!/usr/bin/env python3
"""Find gaps in vendor invoice number sequences. A missing number in an otherwise
sequential series can mean an unrecorded invoice (liability you don't know about)
or a document that was deleted.

Usage: python check.py [path/to/ledger.csv]
Needs columns: invoice_no (like 'LL-1042'), vendor
"""
import re
import sys
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
MIN_INVOICES = 10       # only analyze vendors with a real series
MAX_GAP_REPORT = 20     # ignore huge gaps (vendor probably has other customers)
# ---------------------------

csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path)


def numeric_part(inv):
    m = re.search(r"(\d+)\s*$", str(inv))
    return int(m.group(1)) if m else None


df["seq"] = df["invoice_no"].map(numeric_part)

findings = []
for vendor, grp in df.dropna(subset=["seq"]).groupby("vendor"):
    nums = sorted(grp["seq"].astype(int).unique())
    if len(nums) < MIN_INVOICES:
        continue
    for a, b in zip(nums, nums[1:]):
        gap = b - a - 1
        if 0 < gap <= MAX_GAP_REPORT:
            findings.append({
                "vendor": vendor, "after_invoice": a, "before_invoice": b,
                "missing_count": gap,
                "missing_numbers": ", ".join(str(n) for n in range(a + 1, b)),
            })

out = pd.DataFrame(findings)
print(f"=== Sequence gap check: {len(out)} gap(s) found ===")
if not out.empty:
    print(out.to_string(index=False))
    out.to_csv(Path(__file__).parent / "findings_sequence_gaps.csv", index=False)
    print(f"\nTotal missing invoice numbers: {out['missing_count'].sum()}")
