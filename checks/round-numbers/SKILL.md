# Round number check

**What it finds:** Vendors where a large share of invoices are perfectly round amounts (10,000.00, 25,000.00). Real invoices have VAT lines, unit prices and hours on them — they almost never land round. Round amounts cluster in estimates, retainers without documentation, and fabricated invoices.

**Why it matters:** A vendor billing round numbers repeatedly is either on an undocumented flat retainer (worth reviewing the contract) or worth a closer look for fraud. Auditors run exactly this test.

## Run it

```
python check.py
python check.py my_ap_export.csv
```

Required columns: `invoice_no`, `invoice_date`, `vendor`, `amount`.

## Output

Vendor-level summary (share of round invoices, round spend) + detail rows in `findings_round_numbers.csv`.

## Tune it

- `ROUND_TO` (default 1000): set to 500 or 100 for smaller-ticket ledgers.
- `MIN_ROUND_INVOICES` / `MIN_ROUND_SHARE`: raise both to cut noise on small vendors.

**Known noise source:** legit flat-fee arrangements (rent, retainers, subscriptions). The point isn't "round = fraud", it's "round + no contract on file = ask questions".
