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
