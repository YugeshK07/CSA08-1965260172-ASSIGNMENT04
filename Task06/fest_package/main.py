from pathlib import Path
from fest.processor import build_master
from fest.writer import write_outputs

DEPARTMENTS = ["CSE", "ECE", "MECH", "EEE", "CIVIL"]

def main():
    here = Path(__file__).resolve().parent
    input_folder = here / "input"
    output_folder = here / "output"
    registrations, errors, duplicates = build_master(input_folder, DEPARTMENTS)
    write_outputs(registrations, errors, duplicates, output_folder)
    print("College Fest Registration Desk completed.")
    print(f"Valid unique registrations: {len(registrations)}")
    print(f"Duplicate registrations ignored: {duplicates}")
    print(f"Errors logged: {len(errors)}")
    print(f"Output folder: {output_folder}")

if __name__ == "__main__":
    main()
