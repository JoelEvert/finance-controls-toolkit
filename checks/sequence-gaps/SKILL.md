# Sequence gap check

**What it finds:** Missing numbers in a vendor's invoice sequence as recorded in YOUR ledger. If you have LL-1041 and LL-1043 but no LL-1042, either that invoice never reached you (unrecorded liability waiting to surprise you), it's stuck in someone's inbox, or it was deleted.

**Why it matters:** Completeness is half of AP control. Duplicates cost you money you can see; missing invoices cost you accruals you can't. This is also a classic auditor test on your own outgoing invoice series (sales side) — point it at your AR export too.

## Run it

```
python check.py
python check.py my_ap_export.csv
```

Required columns: `invoice_no`, `vendor`. The script extracts the trailing number from each invoice_no automatically.

## Output

Gaps per vendor with the exact missing numbers. Saved to `findings_sequence_gaps.csv`.

## Tune it

- `MIN_INVOICES` (default 10): vendors with fewer invoices don't have a meaningful series.
- `MAX_GAP_REPORT` (default 20): most vendors invoice other customers too, so their series has natural holes. Small gaps on a vendor that otherwise runs dense sequences are the interesting signal. For your own AR series, set this high — every gap matters there.

**Known noise source:** vendors whose invoice numbers aren't sequential per customer. If a vendor shows dozens of small gaps, their numbering just isn't dedicated to you — ignore them.
