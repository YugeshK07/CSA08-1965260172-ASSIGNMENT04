from pathlib import Path
from collections import defaultdict
from datetime import date
import csv
import sys


def process_month(folder, output_folder):
    folder = Path(folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    counts = defaultdict(lambda: {"P": 0, "A": 0})
    errors = []
    files = sorted(folder.glob("*.txt"))

    for file_path in files:
        try:
            with file_path.open("r", encoding="utf-8") as file:
                for line_no, raw in enumerate(file, start=1):
                    line = raw.strip()
                    if not line:
                        errors.append((file_path.name, line_no, "empty line"))
                        continue
                    fields = [item.strip() for item in line.split(",")]
                    if len(fields) != 3:
                        errors.append((file_path.name, line_no,
                                       f"expected 3 fields, found {len(fields)}"))
                        continue
                    register, date_text, status = fields
                    try:
                        date.fromisoformat(date_text)
                    except ValueError:
                        errors.append((file_path.name, line_no, "invalid date"))
                        continue
                    if not register:
                        errors.append((file_path.name, line_no, "empty register number"))
                        continue
                    if status not in ("P", "A"):
                        errors.append((file_path.name, line_no,
                                       f"invalid status {status!r}"))
                        continue
                    counts[register][status] += 1
        except FileNotFoundError:
            errors.append((file_path.name, 0, "file not found"))
        except (PermissionError, UnicodeDecodeError, OSError) as exc:
            errors.append((file_path.name, 0, f"{type(exc).__name__}: {exc}"))

    with (output_folder / "attendance_report.csv").open(
            "w", newline="", encoding="utf-8") as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["Register Number", "Present", "Absent",
                         "Valid Days", "Attendance Percentage"])
        for register in sorted(counts):
            present = counts[register]["P"]
            absent = counts[register]["A"]
            valid_days = present + absent
            percentage = (present / valid_days * 100) if valid_days else 0
            writer.writerow([register, present, absent, valid_days,
                             f"{percentage:.2f}"])

    with (output_folder / "below_75_percent.txt").open(
            "w", encoding="utf-8") as low_file:
        for register in sorted(counts):
            present = counts[register]["P"]
            total = present + counts[register]["A"]
            if total and present / total * 100 < 75:
                low_file.write(f"{register}: {present / total * 100:.2f}%\n")

    with (output_folder / "damaged_lines.log").open(
            "w", encoding="utf-8") as log:
        for filename, line_no, message in errors:
            log.write(f"{filename}: line {line_no}: {message}\n")

    return counts, errors


if __name__ == "__main__":
    data_dir = Path(__file__).with_name("daily_files")
    out_dir = Path(__file__).with_name("output")
    result, problems = process_month(data_dir, out_dir)
    print(f"Students processed: {len(result)}")
    print(f"Damaged records: {len(problems)}")
    print("Reports written to output/")
