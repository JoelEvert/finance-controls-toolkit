# Threshold splitting check

**What it finds:** Repeated invoices from the same vendor, posted by the same person, all landing just under your approval limit within a short window. Five invoices at 9,760-9,990 against a 10,000 limit is not a coincidence — it's a 49,000 purchase split to avoid sign-off.

**Why it matters:** This is the most common way approval controls get bypassed, and it's invisible invoice-by-invoice. Only the pattern reveals it.

## Run it

```
python check.py
python check.py my_ap_export.csv
```

Required columns: `invoice_no`, `invoice_date`, `vendor`, `amount`, `posted_by`. If you don't have a requester column, map whatever you have (department, cost center) to `posted_by`.

## Output

One row per suspicious vendor/requester pattern with count, date span and total; detail invoices in `findings_threshold_splitting.csv`.

## Tune it

- `APPROVAL_LIMIT`: set to YOUR limit — this is the one config that must be changed before running on real data.
- `UNDER_BAND` (default 5%): widen to 10% for cruder splitters.
- `MIN_HITS` / `WINDOW_DAYS`: 3 hits in 60 days is conservative; 2 in 30 is aggressive.

**Known noise source:** vendors whose genuine unit price sits just under your limit (e.g. a standard license at 9,900). Check the amounts column — identical repeated amounts are more likely legit pricing; varied near-limit amounts are the red flag.
