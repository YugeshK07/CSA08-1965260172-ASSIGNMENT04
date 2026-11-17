# Task 2 – Biometric attendance files

Input format: `register_number,YYYY-MM-DD,P-or-A`, one record per line.
Place all daily `.txt` files in `daily_files/`.

Run: `python attendance_processor.py`

Outputs: `output/attendance_report.csv`, `output/below_75_percent.txt`,
and `output/damaged_lines.log`. Attendance percentage is present records divided
by valid P/A records for that student, multiplied by 100.
