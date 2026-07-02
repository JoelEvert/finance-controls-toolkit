#!/usr/bin/env python3
"""Benford's law test: in natural financial data, ~30% of amounts start with 1
and only ~5% start with 9. Fabricated or manipulated numbers break this pattern.

Usage: python check.py [path/to/ledger.csv]
Needs columns: vendor, amount
"""
import sys
from math import log10
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
MIN_INVOICES = 25    # per-vendor test needs a reasonable sample
MAD_THRESHOLD = 0.06 # flag above this. 0.015 is the classic cutoff for LARGE samples;
                     # small per-vendor samples (~30 invoices) deviate naturally, so default higher
HIGH_DIGITS_ONLY = True  # only flag vendors overusing digits 7-9 (the fraud-relevant pattern)
# ---------------------------

BENFORD = {d: log10(1 + 1 / d) for d in range(1, 10)}

csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path)
df["first_digit"] = df["amount"].astype(str).str.lstrip("0.").str[0].astype(int)


def mad(series):
    observed = series.value_counts(normalize=True)
    return sum(abs(observed.get(d, 0) - BENFORD[d]) for d in range(1, 10)) / 9


findings = []
for vendor, grp in df.groupby("vendor"):
    if len(grp) < MIN_INVOICES:
        continue
    score = mad(grp["first_digit"])
    obs = grp["first_digit"].value_counts(normalize=True)
    worst = max(range(1, 10), key=lambda d: obs.get(d, 0) - BENFORD[d])
    if score > MAD_THRESHOLD and (not HIGH_DIGITS_ONLY or worst >= 7):
        findings.append({
            "vendor": vendor, "invoices": len(grp), "mad_score": round(score, 4),
            "most_overrepresented_digit": worst,
            "share_of_digit": f"{obs.get(worst, 0):.0%} (expected {BENFORD[worst]:.0%})",
        })

out = pd.DataFrame(findings).sort_values("mad_score", ascending=False) if findings else pd.DataFrame()
overall = mad(df["first_digit"])
print("=== Benford's law check ===")
print(f"Whole ledger MAD: {overall:.4f} (threshold {MAD_THRESHOLD})")
print(f"Vendors flagged: {len(out)}")
if not out.empty:
    print(out.to_string(index=False))
    out.to_csv(Path(__file__).parent / "findings_benford.csv", index=False)
