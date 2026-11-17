from pathlib import Path


def save_returns(books, log_filename):
    """Append returned books; each book is written on a separate line."""
    with open(log_filename, "a", encoding="utf-8") as log:
        for book in books:
            log.write(book.rstrip("\n") + "\n")


def process(day_file, log_filename, error_filename):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = [line.strip() for line in source if line.strip()]
        save_returns(books, log_filename)
        return True
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
        with open(error_filename, "a", encoding="utf-8") as error_log:
            error_log.write(f"{day_file}: {type(exc).__name__}: {exc}\n")
        return False


def main():
    folder = Path(__file__).with_name("daily_returns")
    log_file = Path(__file__).with_name("returns.log")
    error_file = Path(__file__).with_name("errors.log")

    # Start this demonstration with clean logs.
    log_file.write_text("", encoding="utf-8")
    error_file.write_text("", encoding="utf-8")

    days = ["day1.txt", "day2.txt", "day3.txt", "missing_day.txt"]
    for day in days:
        success = process(folder / day, log_file, error_file)
        print(f"{day}: {'processed' if success else 'error logged'}")

    print("\nFinal return log:")
    print(log_file.read_text(encoding="utf-8"))
    print("Error log:")
    print(error_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
