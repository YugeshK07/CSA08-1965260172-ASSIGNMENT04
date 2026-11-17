from pathlib import Path

def read_attendance(folder):
    records = {}
    for path in sorted(Path(folder).glob("*.txt")):
        with path.open(encoding="utf-8") as file:
            for line_no, line in enumerate(file, 1):
                fields = [x.strip() for x in line.strip().split(",")]
                if len(fields) != 3 or fields[2] not in ("P", "A"):
                    continue
                register, day, status = fields
                records.setdefault(register, {})[day] = status
    return records


def calculate_stats(records):
    result = {}
    for register, days in records.items():
        present = sum(status == "P" for status in days.values())
        total = len(days)
        result[register] = {
            "present": present,
            "absent": total - present,
            "percentage": (present / total * 100) if total else 0.0,
            "three_consecutive_absences": has_three_consecutive_absences(days)
        }
    return result


def has_three_consecutive_absences(days):
    dates = sorted(days)
    for index in range(len(dates) - 2):
        first, second, third = dates[index:index + 3]
        if days[first] == days[second] == days[third] == "A":
            from datetime import date
            d1, d2, d3 = date.fromisoformat(first), date.fromisoformat(second), date.fromisoformat(third)
            if (d2 - d1).days == 1 and (d3 - d2).days == 1:
                return True
    return False


from pathlib import Path

def write_reports(stats, output_folder):
    out = Path(output_folder)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "attendance_summary.txt").open("w", encoding="utf-8") as file:
        file.write("Register,Present,Absent,Attendance %\n")
        for register, item in sorted(stats.items()):
            file.write(f"{register},{item['present']},{item['absent']},{item['percentage']:.2f}\n")
    with (out / "three_day_absence.txt").open("w", encoding="utf-8") as file:
        for register, item in sorted(stats.items()):
            if item["three_consecutive_absences"]:
                file.write(register + "\n")
