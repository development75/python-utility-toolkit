from pathlib import Path
import shutil

from file_categories import FILE_CATEGORIES


def get_category(file_path: Path) -> str:
    """Return the category for a file based on its extension."""

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"

def get_unique_path(destination: Path) -> Path:
    """Avoid overwriting a file that already exists."""

    if not destination.exists():
        return destination

    count = 1
    while True:
        new_destination = destination.with_name(
            f"{destination.stem}_{count}{destination.suffix}"
        )
        if not new_destination.exists():
            return new_destination
        count += 1

def organize_files(source_directory: str, dry_run: bool = False) -> dict:
    """Organize files by extension, optionally previewing changes."""

    source = Path(source_directory).expanduser().resolve()

    if not source.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {source}"
        )

    summary = {
        "detected": 0,
        "moved": 0,
        "skipped": 0,
        "errors": 0
    }

    for file_path in source.iterdir():

        if not file_path.is_file():
            continue

        if file_path.is_symlink():
            summary["skipped"] += 1
            continue

        summary["detected"] += 1

        try:
            category = get_category(file_path)

            destination_directory = source / category

            destination = destination_directory / file_path.name

            destination = get_unique_path(destination)

            if dry_run:
                print(
                    f"{file_path.name} -> "
                    f"{category}/{destination.name}"
                )
                summary["skipped"] += 1
                continue

            destination_directory.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.move(
                str(file_path),
                str(destination)
            )

            print(
                f"Moved: {file_path.name} -> "
                f"{category}/{destination.name}"
            )

            summary["moved"] += 1

        except OSError as error:
            print(f"Error processing {file_path.name}: {error}")
            summary["errors"] += 1

    return summary

