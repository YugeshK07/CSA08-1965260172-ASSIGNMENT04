# Task 4 – File and exception forensics

Run: `python return_log.py`

The corrected version opens the log in append mode, writes one newline-terminated
record per book, and uses `with` so files close even if an error occurs. Missing
or unreadable daily files are recorded in `errors.log`; processing continues.
