# Duplicate payment check

**What it finds:** Two invoices from the same vendor for the same amount within a short window — the classic double-payment pattern (invoice paid from both the email copy and the portal copy, or re-keyed after a "where's my money" call).

**Why it matters:** Duplicate payments are the most common recoverable AP leak. Companies applying automated controls report 30-50% drops in undetected duplicates.

## Run it

```
python check.py                    # runs on bundled sample data
python check.py my_ap_export.csv   # runs on your own export
```

Required columns: `invoice_no`, `invoice_date`, `vendor`, `amount`. Export these from any ERP as CSV.

## Output

Console summary + `findings_duplicate_payments.csv` with the paired invoices, dates, and total exposure.

## Tune it

Both knobs are at the top of `check.py`:

- `DAYS_WINDOW` (default 10): widen to 30 to catch slow duplicates, narrow to 3 to cut noise from genuine recurring charges.
- `AMOUNT_TOLERANCE` (default 0.0 = exact): set to 1.0 to catch near-identical amounts (rounding/FX differences).

**Known noise source:** genuine recurring flat fees (rent, subscriptions) trigger this. Filter those vendors out first, or narrow the window.
