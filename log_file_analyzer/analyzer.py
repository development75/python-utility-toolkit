from pathlib import Path

def read_log_file(file_path: str) -> list:
    """Read a log file and return its lines."""


    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Provided path is not a file: {path}")

    with path.open("r", encoding="utf-8") as file:
        log_entries = file.readlines()

    return [line.strip() for line in log_entries if line.strip()]

def count_log_levels(log_entries: list) -> dict:
    """Count occurrences of each log level."""

    log_counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }

    for entry in log_entries:
        for level in log_counts:
            if f" {level} " in entry:
                log_counts[level] += 1
                break

    return log_counts
