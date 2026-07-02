# Benford's law check

**What it finds:** Vendors whose invoice amounts don't follow the natural first-digit distribution. In real financial data ~30% of amounts start with 1, falling to ~5% starting with 9. People inventing numbers unconsciously overuse high digits (8xxx, 9xxx) — especially when padding just under approval limits.

**Why it matters:** It's the most famous forensic accounting test for a reason: it catches fabrication patterns no individual-invoice review would spot. A vendor at 40% amounts starting with 8-9 deserves a closer look.

## Run it

```
python check.py
python check.py my_ap_export.csv
```

Required columns: `vendor`, `amount`.

## Output

Whole-ledger score plus per-vendor flags with the most overrepresented digit. Saved to `findings_benford.csv`. Score = mean absolute deviation (MAD) from Benford; 0.015 is the standard "nonconformity" cutoff.

## Tune it

- `MIN_INVOICES` (default 25): Benford needs sample size — don't lower this much or you'll flag noise.
- `MAD_THRESHOLD` (default 0.06): the textbook cutoff is 0.015, but that assumes hundreds of data points. Per-vendor samples of ~30 invoices deviate naturally, so the default is deliberately higher. Running on a whole ledger (thousands of rows)? Drop it toward 0.015.
- `HIGH_DIGITS_ONLY` (default True): only flags vendors overusing digits 7-9, which is the fraud-relevant pattern (people padding numbers under limits). Set False to see all deviations.

**Known noise sources:** Benford assumes amounts spanning multiple orders of magnitude. A vendor with fixed pricing (every invoice 4,500) will "deviate" innocently. Same for round-retainer vendors — cross-check with the round-numbers check before drawing conclusions. Treat this as a "where to look" tool, never as proof.
