from analyzer import read_log_file, count_log_levels

def main():
    print("Starting Log File Analyzer...")
    
    file_path = "./sample_files/application.log"

    try:
        log_entries = read_log_file(file_path)

        log_counts = count_log_levels(log_entries)

        print("\nLOG FILE ANALYZER")
        print("=" * 50)

        print(f"Total log entries: {len(log_entries)}")

        print("\nLOG LEVEL SUMMARY")
        print("-" * 50)

        for level, count in log_counts.items():
            print(f"{level:<12}: {count}")

        print(f"{'TOTAL':<12}: {sum(log_counts.values())}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
