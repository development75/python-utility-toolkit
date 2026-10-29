from pathlib import Path
import shutil

from smart_file_organizer.file_categories import FILE_CATEGORIES


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

def organize_files(source_directory: str) -> dict:
    """Organize files into folders based on their extensions."""
    source = Path(source_directory).expenduser().resolve()

    if not source.exist():
        raise FileNotFoundError( f"Directory does not exist: {source}" )
    if not source.is_dir():
        raise NotADirectoryError( f"Not a directory: {source}" )

    summary = {
        "moved": 0,
        "skipped": 0,
        "errors": 0
    }
    for file_path in source.iterdir():
        # Process files only, not directories.
        if not file_path.is_file():
            continue
        # Skip symbolic links for safety.
        if file_path.is_symlink():
            summary["skipped"] += 1
            continue
        try:
            category = get_category(file_path)
            destination_directory = source / category
            destination_directory.mkdir(
                parents = True,
                exist_ok = True
            )
            destination = destination_directory / file_path.name
            destination = get_unique_path(destination)

            shutil.move(
                str(file_path),
                str(destination)
            )
            print(
                f"Moved: {file_path.name} -> {category}/"
                f"{destination.name}"
            )

            summary["moved"] += 1

        except OSError as error:
            print(f"Error processing {file_path.name}: {error}")
            summary["errors"] += 1

        return summary