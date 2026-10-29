import argparse

from organizer import organize_files


def main():
    parser = argparse.ArgumentParser(
        description="Smart File Organizer"
    )
    parser.add_argument(
        "directory",
        help="Directory containing files to organize"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file movements without moving files"
    )
    args = parser.parse_args()

    try:
        print("\nSMART FILE ORGANIZER")
        print("====================")

        if args.dry_run:
            print("Mode: DRY RUN\n")
        else:
            print("Mode: ORGANIZE\n")

        summary = organize_files(
            args.directory,
            dry_run=args.dry_run
        )

        print("\nSUMMARY")
        print("-------")
        print(f"Files detected: {summary['detected']}")
        print(f"Files moved: {summary['moved']}")
        print(f"Errors: {summary['errors']}")

        if args.dry_run:
            print("\nDry run completed. No files were moved.")
        else:
            print("\nOrganization completed!")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
