#!/usr/bin/env python3
"""Run every check in this folder against one ledger export.

Usage: python run_all.py [path/to/ledger.csv]
"""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).parent
target = sys.argv[1:2] or []

checks = sorted(p for p in here.iterdir() if p.is_dir() and (p / "check.py").exists())
print(f"Running {len(checks)} checks...\n")
for check in checks:
    print("=" * 70)
    subprocess.run([sys.executable, str(check / "check.py"), *target])
    print()
print("=" * 70)
print("Done. Findings CSVs are saved inside each check's folder.")
