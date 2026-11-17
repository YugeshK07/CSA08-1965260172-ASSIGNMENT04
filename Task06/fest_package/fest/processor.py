from .reader import read_department_files
from .validation import parse_registration

def build_master(folder, departments):
    registrations = {}
    errors = []
    duplicate_count = 0

    for filename, line_no, raw_line in read_department_files(folder, departments):
        if line_no == 0 and raw_line.startswith("__FILE_ERROR__:"):
            errors.append((filename, line_no, raw_line))
            continue
        try:
            record = parse_registration(raw_line)
            register = record["register"]
            if register in registrations:
                duplicate_count += 1
                errors.append((filename, line_no,
                               f"duplicate register number {register}; ignored"))
                continue
            registrations[register] = record
        except ValueError as exc:
            errors.append((filename, line_no, str(exc)))

    for missing in getattr(read_department_files, "missing_files", []):
        errors.append((missing, 0, "department file is missing"))

    return registrations, errors, duplicate_count
