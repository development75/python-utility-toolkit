from pathlib import Path
from collections import defaultdict
import hashlib


def calculate_file_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def files_are_identical(
    first_file: Path,
    second_file: Path
) -> bool:
    """Compare two files byte by byte."""

    try:
        if first_file.stat().st_size != second_file.stat().st_size:
            return False

        with first_file.open("rb") as first:
            with second_file.open("rb") as second:

                while True:
                    first_chunk = first.read(1024 * 1024)
                    second_chunk = second.read(1024 * 1024)

                    if first_chunk != second_chunk:
                        return False

                    if not first_chunk:
                        return True

    except OSError as error:
        print(f"Could not compare files: {error}")
        return False


def find_duplicates(directory: str) -> dict:
    """Find duplicate files using size, SHA-256, and content comparison."""

    source = Path(directory).expanduser().resolve()

    if not source.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {source}"
        )

    files_by_size = defaultdict(list)

    files_scanned = 0
    files_skipped = 0
    errors = 0

    # Group files by size first.
    for file_path in source.rglob("*"):

        if file_path.is_symlink():
            files_skipped += 1
            continue

        if not file_path.is_file():
            continue

        try:
            file_size = file_path.stat().st_size

            files_by_size[file_size].append(file_path)
            files_scanned += 1

        except OSError as error:
            print(f"Cannot access {file_path}: {error}")
            errors += 1

    # Calculate hashes only for files sharing a size.
    files_by_hash = defaultdict(list)

    for file_size, file_paths in files_by_size.items():

        if len(file_paths) < 2:
            continue

        for file_path in file_paths:

            try:
                file_hash = calculate_file_hash(file_path)

                files_by_hash[
                    (file_size, file_hash)
                ].append(file_path)

            except OSError as error:
                print(f"Cannot read {file_path}: {error}")
                errors += 1

    # Verify file contents before grouping duplicates.
    duplicate_groups = []

    for file_paths in files_by_hash.values():

        if len(file_paths) < 2:
            continue

        verified_groups = []

        for file_path in file_paths:

            for group in verified_groups:

                if files_are_identical(file_path, group[0]):
                    group.append(file_path)
                    break

            else:
                verified_groups.append([file_path])

        duplicate_groups.extend(
            group for group in verified_groups
            if len(group) > 1
        )

    duplicate_file_count = sum(
        len(group) - 1
        for group in duplicate_groups
    )

    wasted_space = sum(
        file_path.stat().st_size * (len(group) - 1)
        for group in duplicate_groups
        for file_path in [group[0]]
    )

    return {
        "files_scanned": files_scanned,
        "duplicate_groups": duplicate_groups,
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_file_count": duplicate_file_count,
        "wasted_space_bytes": wasted_space,
        "files_skipped": files_skipped,
        "errors": errors,
    }
