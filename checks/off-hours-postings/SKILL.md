# Off-hours posting check

**What it finds:** Entries posted on weekends or late at night. Standard audit test for management override, unauthorized access, and rushed period-end adjustments nobody reviewed.

**Why it matters:** Most off-hours entries are innocent (deadline crunch, time zones, scheduled jobs). But if fraud happens, it disproportionately happens when nobody's watching — so a quick scan of this list each month is cheap insurance. The per-user summary shows whether one person owns the pattern.

## Run it

```
python check.py
python check.py my_gl_export.csv
```

Required columns: `invoice_no`, `vendor`, `amount`, `posted_by`, `posted_at` (a timestamp — most ERPs export "created at" or "entry timestamp").

## Output

Flagged entries with reason (weekend / after-hours / both) + per-user counts. Saved to `findings_off_hours.csv`.

## Tune it

- `WORK_START` / `WORK_END` (default 06-20): match your team's real hours.
- `FLAG_WEEKENDS`: set to `False` if weekend posting is normal in your shop.

**Known noise source:** automated integrations that post at fixed odd hours (bank feeds at 02:00). Filter those system users out, or note them once and ignore.
