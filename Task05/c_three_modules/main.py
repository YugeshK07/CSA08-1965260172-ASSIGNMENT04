from pathlib import Path
from reader import read_attendance
from stats import calculate_stats
from report import write_reports

if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    stats = calculate_stats(read_attendance(here / "data"))
    write_reports(stats, Path(__file__).with_name("output"))
    print(f"Processed {len(stats)} students using three modules.")
