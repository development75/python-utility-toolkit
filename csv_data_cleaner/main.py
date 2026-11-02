from cleaner import read_csv_file


def main():
    print("Starting CSV Data Cleaner...")

    file_path = "./sample_files/employees.csv"

    try:
        records = read_csv_file(file_path)

        print("\nCSV DATA CLEANER")
        print("=" * 45)

        print(f"Total records: {len(records)}")

        print("\nCSV RECORDS")
        print("-" * 45)

        for record in records:
            print(record)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()