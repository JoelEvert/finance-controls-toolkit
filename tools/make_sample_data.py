#!/usr/bin/env python3
"""Generate a realistic sample AP ledger with seeded anomalies for testing the checks.

Every anomaly the checks are supposed to catch is planted here on purpose,
so you can verify a check works before pointing it at real data.

Usage: python make_sample_data.py            (writes ../checks/sample_data/ap_ledger.csv)
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT = Path(__file__).parent.parent / "checks" / "sample_data" / "ap_ledger.csv"

VENDORS = [
    ("Nordic Supplies ApS", "NS", 500, 15000),
    ("Vestergaard IT A/S", "VIT", 2000, 30000),
    ("Kastrup Consulting", "KC", 5000, 60000),
    ("Lyngby Logistik A/S", "LL", 800, 12000),
    ("Ørsted Kontorartikler", "OK", 150, 4000),
    ("Bruun & Berg Advokater", "BB", 8000, 45000),
    ("CloudDane Hosting", "CD", 1200, 9000),
    ("Møller Ejendomme A/S", "ME", 18000, 55000),
    ("Fyn Catering ApS", "FC", 400, 6000),
    ("Aarhus Marketing Group", "AM", 3000, 25000),
]
STAFF = ["mette.j", "lars.p", "sofie.k", "jonas.h"]
START = datetime(2026, 1, 2)


def business_dt():
    """Random business-hours timestamp Jan-Jun 2026 (weekdays 08-17)."""
    while True:
        d = START + timedelta(days=random.randint(0, 178))
        if d.weekday() < 5:
            return d.replace(hour=random.randint(8, 16), minute=random.randint(0, 59))


rows = []
counters = {prefix: 1000 for _, prefix, _, _ in VENDORS}


def add(vendor, prefix, amount, posted_dt, invoice_no=None, posted_by=None, inv_date=None):
    if invoice_no is None:
        counters[prefix] += 1
        invoice_no = f"{prefix}-{counters[prefix]}"
    rows.append({
        "invoice_no": invoice_no,
        "invoice_date": (inv_date or posted_dt).strftime("%Y-%m-%d"),
        "vendor": vendor,
        "amount": f"{amount:.2f}",
        "currency": "DKK",
        "posted_by": posted_by or random.choice(STAFF),
        "posted_at": posted_dt.strftime("%Y-%m-%d %H:%M"),
    })
    return invoice_no


# --- baseline: ~340 ordinary invoices ---
for vendor, prefix, lo, hi in VENDORS:
    for _ in range(34):
        amt = round(random.uniform(lo, hi), 2)
        add(vendor, prefix, amt, business_dt())

# --- seed 1: duplicate payments (same vendor+amount, new invoice_no, days apart) ---
for i in [5, 60, 200]:
    src = rows[i]
    dt = datetime.strptime(src["posted_at"], "%Y-%m-%d %H:%M") + timedelta(days=random.randint(2, 5))
    prefix = src["invoice_no"].split("-")[0]
    add(src["vendor"], prefix, float(src["amount"]), dt)

# --- seed 2: near-duplicate vendor names ---
for _ in range(4):
    add("Nordic Supplies APS", "NS", round(random.uniform(500, 15000), 2), business_dt())
for _ in range(3):
    add("Moeller Ejendomme A/S", "ME", round(random.uniform(18000, 55000), 2), business_dt())

# --- seed 3: suspiciously round amounts (Kastrup Consulting) ---
for amt in [5000, 10000, 15000, 20000, 25000, 10000, 15000, 20000]:
    add("Kastrup Consulting", "KC", float(amt), business_dt())

# --- seed 4: threshold splitting (just under 10,000 approval limit, same requester) ---
base = datetime(2026, 4, 7, 10, 30)
for i, amt in enumerate([9850.00, 9920.00, 9760.00, 9990.00, 9875.00]):
    add("Vestergaard IT A/S", "VIT", amt, base + timedelta(days=i * 4), posted_by="jonas.h")

# --- seed 5: off-hours postings (weekend + late night) ---
add("CloudDane Hosting", "CD", 4200.00, datetime(2026, 3, 14, 23, 40))   # Sat night
add("CloudDane Hosting", "CD", 3100.00, datetime(2026, 3, 15, 2, 15))    # Sun 02:15
add("Fyn Catering ApS", "FC", 1850.00, datetime(2026, 5, 2, 22, 30))     # Sat 22:30
add("Bruun & Berg Advokater", "BB", 22000.00, datetime(2026, 2, 8, 23, 5))  # Sun 23:05

# --- seed 6: gaps in Lyngby Logistik invoice sequence (remove 3 recorded invoices) ---
ll = [r for r in rows if r["vendor"] == "Lyngby Logistik A/S"]
for victim in random.sample(ll, 3):
    rows.remove(victim)

# --- seed 7: Benford skew (Aarhus Marketing: pile of 8xxx/9xxx amounts) ---
for _ in range(18):
    amt = round(random.uniform(8000, 9999), 2)
    add("Aarhus Marketing Group", "AM", amt, business_dt())

random.shuffle(rows)
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} rows -> {OUT}")
