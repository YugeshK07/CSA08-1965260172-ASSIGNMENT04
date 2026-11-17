# Task 1 – File-processing design review

Run: `python diagnose_repair.py`

The program reads one record at a time, validates the three fields, uses `Decimal`
for currency, closes files through `with`, writes valid records incrementally and
stores rejected line numbers and reasons separately.
