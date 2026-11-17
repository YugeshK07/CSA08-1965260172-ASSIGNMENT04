from pathlib import Path
from attendance_utils import read_attendance, calculate_stats, write_reports

if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    stats = calculate_stats(read_attendance(here / "data"))
    write_reports(stats, Path(__file__).with_name("output"))
    print(f"Processed {len(stats)} students using one imported module.")
