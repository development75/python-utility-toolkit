import csv
from pathlib import Path

def read_csv_file(file_path: str) -> list:
    """Read CSV data and return records as a list of dictionaries."""


    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Provided path is not a file: {path}")

    records = []

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing a header row.")

        for row in reader:
            cleaned_row = {
                key.strip(): value.strip() if value is not None else ""
                for key, value in row.items()
                if key is not None
            }

        records.append(cleaned_row)

    return records
