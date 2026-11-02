import csv
import json
from pathlib import Path

def csv_to_json(input_file: str, output_file: str) -> int:
    """Convert a CSV file into JSON format."""


    source = Path(input_file)
    destination = Path(output_file)

    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    if not source.is_file():
        raise ValueError(f"Input path is not a file: {source}")

    if source.suffix.lower() != ".csv":
        raise ValueError("Input file must have a .csv extension.")

    records = []

    with source.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing headers.")

        for row in reader:
            records.append(row)

    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    return len(records)

def json_to_csv(input_file: str, output_file: str) -> int:
    """Convert a JSON file containing records into CSV format."""

    source = Path(input_file)
    destination = Path(output_file)

    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    if not source.is_file():
        raise ValueError(f"Input path is not a file: {source}")

    if source.suffix.lower() != ".json":
        raise ValueError("Input file must have a .json extension.")

    with source.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("JSON data must contain a list of records.")

    if not records:
        raise ValueError("JSON file contains no records.")

    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every JSON record must be an object.")

    fieldnames = list(dict.fromkeys(
        key for record in records for key in record
    ))

    if not fieldnames:
        raise ValueError("JSON records do not contain any fields.")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return len(records)

