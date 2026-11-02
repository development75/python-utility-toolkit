from converter import csv_to_json, json_to_csv

def main():
    print("Starting File Converter...")

    try:
        # CSV to JSON
        csv_input = "./sample_files/employees.csv"
        json_output = "./converted_files/employees.json"

        csv_records = csv_to_json(csv_input, json_output)

        print("\nCSV TO JSON")
        print("-" * 45)
        print(f"Input file: {csv_input}")
        print(f"Output file: {json_output}")
        print(f"Records converted: {csv_records}")

        # JSON to CSV
        json_input = "./sample_files/sample.json"
        csv_output = "./converted_files/employees_from_json.csv"

        json_records = json_to_csv(json_input, csv_output)

        print("\nJSON TO CSV")
        print("-" * 45)
        print(f"Input file: {json_input}")
        print(f"Output file: {csv_output}")
        print(f"Records converted: {json_records}")

        print("\nAll conversions completed successfully!")

    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"\nConversion failed: {error}")

    except json.JSONDecodeError as error:
        print(f"\nInvalid JSON file: {error}")


if __name__ == "__main__":
    main()
