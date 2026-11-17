# Task 5 – The same utility organised four ways

The shared sample files are in `data/`. Run each organisation from its own folder:

1. `python a_single_script/attendance_all_in_one.py`
2. `cd b_one_module` then `python main.py`
3. `cd c_three_modules` then `python main.py`
4. `cd d_package` then `python main.py`

Each version produces `attendance_summary.txt` and `three_day_absence.txt`.
The third report identifies students absent on three consecutive calendar dates.
All versions use the same logic, so the comparison focuses on organisation,
readability, reuse and testing rather than different results.
