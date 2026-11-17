from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys


def process_mess_bills(filename, report_filename="mess_report.txt",
                       rejected_filename="rejected_lines.txt"):
    """Read mess bills safely, write valid report rows, and total valid amounts."""
    total = Decimal("0.00")
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as source, \
             open(report_filename, "w", encoding="utf-8") as report:
            for line_number, raw_line in enumerate(source, start=1):
                line = raw_line.strip()

                if not line:
                    rejected.append((line_number, "empty line", raw_line.rstrip("\n")))
                    continue

                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 3:
                    rejected.append((line_number, "expected 3 comma-separated fields",
                                     raw_line.rstrip("\n")))
                    continue

                register_no, name, amount_text = parts
                if not register_no or not name:
                    rejected.append((line_number, "register number/name is empty",
                                     raw_line.rstrip("\n")))
                    continue

                try:
                    amount = Decimal(amount_text)
                    if not amount.is_finite() or amount < 0:
                        raise InvalidOperation
                except InvalidOperation:
                    rejected.append((line_number, f"invalid amount: {amount_text!r}",
                                     raw_line.rstrip("\n")))
                    continue

                total += amount
                report.write(f"{register_no},{name},{amount:.2f}\n")

    except FileNotFoundError:
        raise
    except PermissionError:
        raise

    with open(rejected_filename, "w", encoding="utf-8") as rejected_file:
        for number, reason, original in rejected:
            rejected_file.write(f"Line {number}: {reason} | {original}\n")

    return total, rejected


def main():
    sample = Path(__file__).with_name("mess_oct.txt")
    try:
        total, rejected = process_mess_bills(sample)
        print("Valid mess bill total:", f"{total:.2f}")
        print("Rejected records:", len(rejected))
        print("Valid report saved to mess_report.txt")
        print("Rejected lines saved to rejected_lines.txt")
    except (FileNotFoundError, PermissionError, OSError) as error:
        print(f"File processing failed: {error}")


if __name__ == "__main__":
    main()
