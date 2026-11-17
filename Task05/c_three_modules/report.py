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
