# Task 6 – College Fest Registration Desk

Run from this folder: `python fest_package/main.py`

Expected input format (one registration per line):
`register_number,name,department,email,event1;event2`

The package separates reading, validation, processing and output writing.
The sample data intentionally includes a duplicate register number, an invalid
email, a malformed line and a missing CIVIL department file. The program continues
processing and writes a master CSV, one CSV per event, a summary and an error log.
