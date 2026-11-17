import os
import tempfile
from datetime import date


class InvalidRecord(Exception):
    """Raised when an attendance line does not match the expected format."""


class AttendanceFileError(Exception):
    """Raised when an attendance file cannot be processed."""


def parse_line(line):
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, day, status = parts
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status {status!r}")
    if not register or not day:
        raise InvalidRecord("register number and date must not be empty")
    try:
        date.fromisoformat(day)
    except ValueError as exc:
        raise InvalidRecord(f"invalid date {day!r}") from exc
    return register, day, status


def summarise(path):
    present = 0
    absent = 0
    errors = []
    source = None

    try:
        source = open(path, "r", encoding="utf-8")
        for line_number, line in enumerate(source, start=1):
            try:
                _register, _day, status = parse_line(line)
                if status == "P":
                    present += 1
                else:
                    absent += 1
            except InvalidRecord as exc:
                errors.append((line_number, str(exc)))
    except (OSError, UnicodeDecodeError) as exc:
        try:
            raise AttendanceFileError(f"cannot process file {path}") from exc
        except AttendanceFileError as wrapped:
            cause_name = type(wrapped.__cause__).__name__
            errors.append((0, f"{wrapped} (cause: {cause_name})"))
    else:
        # This block runs only when the file was read without a file-level error.
        pass
    finally:
        if source is not None:
            source.close()

    return present, absent, errors


if __name__ == "__main__":
    data = (
        "192311001,2026-10-08,P\n"
        "192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n"
        "192311004,2026-10-08,L\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                     encoding="utf-8") as temp:
        temp.write(data)
        filename = temp.name

    try:
        print(summarise(filename))
        print(summarise(filename + ".missing"))
    finally:
        os.remove(filename)
