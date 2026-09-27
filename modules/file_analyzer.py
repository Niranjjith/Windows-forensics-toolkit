from pathlib import Path
from datetime import datetime
import hashlib


BUFFER_SIZE = 1024 * 1024


def calculate_hash(file_path, algorithm="sha256"):
    """
    Calculate the cryptographic hash of a file.

    Supported algorithms:
    - MD5
    - SHA-1
    - SHA-256
    """

    hash_function = hashlib.new(algorithm)

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)

            if not chunk:
                break

            hash_function.update(chunk)

    return hash_function.hexdigest()


def get_file_type(file_path):
    """
    Return the file extension/type.
    """

    path = Path(file_path)

    if path.suffix:
        return path.suffix.lower()

    return "No extension"


def analyze_file(file_path):
    """
    Collect forensic information about a single file.
    """

    path = Path(file_path)

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    stat = path.stat()

    file_information = {
        "name": path.name,
        "path": str(path.resolve()),
        "extension": get_file_type(path),
        "size": stat.st_size,

        "created": datetime.fromtimestamp(
            stat.st_ctime
        ).isoformat(sep=" ", timespec="seconds"),

        "modified": datetime.fromtimestamp(
            stat.st_mtime
        ).isoformat(sep=" ", timespec="seconds"),

        "accessed": datetime.fromtimestamp(
            stat.st_atime
        ).isoformat(sep=" ", timespec="seconds"),

        "md5": calculate_hash(path, "md5"),
        "sha1": calculate_hash(path, "sha1"),
        "sha256": calculate_hash(path, "sha256"),
    }

    return file_information


def analyze_directory(directory_path):
    """
    Recursively analyze all files inside a directory.
    """

    directory = Path(directory_path)

    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory_path}")

    results = []

    for file_path in directory.rglob("*"):

        if not file_path.is_file():
            continue

        try:
            information = analyze_file(file_path)
            results.append(information)

        except PermissionError:
            print(f"Permission denied: {file_path}")

        except OSError as error:
            print(f"Could not analyze {file_path}: {error}")

    return results