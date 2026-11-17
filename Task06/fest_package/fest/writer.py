from pathlib import Path
import csv

def write_outputs(registrations, errors, duplicate_count, output_folder):
    out = Path(output_folder)
    out.mkdir(parents=True, exist_ok=True)

    with (out / "master_list.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Register Number", "Name", "Department", "Email", "Events"])
        for register in sorted(registrations):
            item = registrations[register]
            writer.writerow([item["register"], item["name"], item["department"],
                             item["email"], ";".join(item["events"])])

    all_events = sorted({event for item in registrations.values()
                         for event in item["events"]})
    for event in all_events:
        safe_name = "".join(ch if ch.isalnum() else "_" for ch in event).strip("_")
        with (out / f"event_{safe_name}.csv").open(
                "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Register Number", "Name", "Department", "Email"])
            for register in sorted(registrations):
                item = registrations[register]
                if event in item["events"]:
                    writer.writerow([item["register"], item["name"],
                                     item["department"], item["email"]])

    counts = {}
    for item in registrations.values():
        counts[item["department"]] = counts.get(item["department"], 0) + 1
    with (out / "summary_report.txt").open("w", encoding="utf-8") as file:
        file.write(f"Valid unique registrations: {len(registrations)}\n")
        file.write(f"Duplicate registrations ignored: {duplicate_count}\n")
        file.write("Registrations by department:\n")
        for department, count in sorted(counts.items()):
            file.write(f"{department}: {count}\n")
        file.write(f"Unique events: {len(all_events)}\n")

    with (out / "error_log.txt").open("w", encoding="utf-8") as file:
        for filename, line_no, message in errors:
            file.write(f"{filename}: line {line_no}: {message}\n")
