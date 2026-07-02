# Vendor name fuzzing

**What it finds:** Vendors that are probably the same company entered twice — "Nordic Supplies ApS" vs "Nordic Supplies APS", "Møller" vs "Moeller". Legal-form suffixes (ApS, A/S) and punctuation are normalized before comparing.

**Why it matters:** Duplicate vendor records are how duplicate payments get past exact-match controls, and they fragment your spend-per-vendor reporting. Fixing the vendor master is usually the highest-leverage AP cleanup.

## Run it

```
python check.py
python check.py my_ap_export.csv
```

Required columns: `vendor`, `amount`.

## Output

Pairs of similar vendor names with invoice counts and total spend for each — so you can see which record is the "real" one to merge into. Saved to `findings_vendor_names.csv`.

## Tune it

- `SIMILARITY_THRESHOLD` (default 0.85): drop to 0.75 to catch sloppier variants, raise to 0.92 if you get false pairs like "Jensen Byg" / "Jansen Byg" that are genuinely different companies.
- Add local legal-form suffixes to the `normalize()` list (GmbH, Ltd, Oy, AB...) if your vendor base isn't Danish.

**Known noise source:** franchises and sister companies legitimately share most of a name. The spend columns help you judge each pair quickly.
