import argparse

from finder import find_duplicates


def format_size(size_bytes: int) -> str:
    """Convert bytes into a readable size."""

    size = float(size_bytes)

    for unit in ("B", "KB", "MB", "GB", "TB"):

        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size_bytes} B"


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files by comparing their contents."
    )

    parser.add_argument(
        "directory",
        help="Directory to scan for duplicate files."
    )

    args = parser.parse_args()

    try:
        result = find_duplicates(args.directory)

        print("\nDUPLICATE FILE FINDER")
        print("=" * 45)

        print(f"Directory scanned: {args.directory}")
        print(f"Files scanned: {result['files_scanned']}")

        print("\nDUPLICATE RESULTS")
        print("-" * 45)

        if result["duplicate_groups"]:

            for number, group in enumerate(
                result["duplicate_groups"], start=1
            ):

                print(f"\nDuplicate Group {number}:")

                for index, file_path in enumerate(group):

                    label = (
                        "Representative"
                        if index == 0
                        else "Duplicate"
                    )

                    print(f"  {label}: {file_path}")
                    print(
                        f"    Size: "
                        f"{format_size(file_path.stat().st_size)}"
                    )

        else:
            print("No duplicate files found.")

        print("\nSUMMARY")
        print("-" * 45)

        print(f"Files scanned: {result['files_scanned']}")
        print(
            f"Duplicate groups: "
            f"{result['duplicate_group_count']}"
        )
        print(
            f"Duplicate files: "
            f"{result['duplicate_file_count']}"
        )
        print(
            f"Potentially reclaimable space: "
            f"{format_size(result['wasted_space_bytes'])}"
        )
        print(f"Files skipped: {result['files_skipped']}")
        print(f"Errors: {result['errors']}")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
