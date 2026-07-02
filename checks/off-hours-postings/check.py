#!/usr/bin/env python3
"""Flag entries posted on weekends or outside business hours. Off-hours postings
are a standard audit red flag for override activity and rushed period-end fixes.

Usage: python check.py [path/to/ledger.csv]
Needs columns: invoice_no, vendor, amount, posted_by, posted_at (timestamp)
"""
import sys
from pathlib import Path
import pandas as pd

# --- CONFIG (edit these) ---
WORK_START = 6   # earliest normal posting hour (06:00)
WORK_END = 20    # latest normal posting hour (20:00)
FLAG_WEEKENDS = True
# ---------------------------

csv_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "sample_data" / "ap_ledger.csv"
df = pd.read_csv(csv_path, parse_dates=["posted_at"])

is_weekend = df["posted_at"].dt.weekday >= 5
is_late = (df["posted_at"].dt.hour < WORK_START) | (df["posted_at"].dt.hour >= WORK_END)
mask = is_late | (is_weekend if FLAG_WEEKENDS else False)

out = df[mask].copy()
out["reason"] = ""
out.loc[is_weekend & mask, "reason"] = "weekend"
out.loc[is_late & ~is_weekend & mask, "reason"] = "after-hours"
out.loc[is_late & is_weekend & mask, "reason"] = "weekend + after-hours"

cols = ["invoice_no", "vendor", "amount", "posted_by", "posted_at", "reason"]
print(f"=== Off-hours posting check: {len(out)} entr(ies) flagged ===")
if not out.empty:
    print(out[cols].sort_values("posted_at").to_string(index=False))
    out[cols].to_csv(Path(__file__).parent / "findings_off_hours.csv", index=False)
    by_user = out.groupby("posted_by").size()
    print("\nBy user:\n" + by_user.to_string())
