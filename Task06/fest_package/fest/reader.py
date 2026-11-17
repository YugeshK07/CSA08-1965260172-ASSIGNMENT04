from pathlib import Path

def read_department_files(folder, departments):
    """Yield (filename, line_number, raw_line); report missing department files."""
    folder = Path(folder)
    missing = []
    for department in departments:
        path = folder / f"{department}.txt"
        if not path.exists():
            missing.append(path.name)
            continue
        try:
            with path.open("r", encoding="utf-8") as source:
                for line_no, line in enumerate(source, start=1):
                    yield path.name, line_no, line.rstrip("\n")
        except (PermissionError, UnicodeDecodeError, OSError) as exc:
            yield path.name, 0, f"__FILE_ERROR__:{type(exc).__name__}:{exc}"
    read_department_files.missing_files = missing
