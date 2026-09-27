from pathlib import Path
from datetime import datetime

from core.hash_engine import (
    calculate_all_hashes
)


def analyze_file(
    file_path,
    case_id,
    evidence_id
):

    path = Path(file_path)

    if not path.is_file():
        raise ValueError(
            f"Not a file: {path}"
        )

    stat = path.stat()

    hashes = calculate_all_hashes(
        path
    )

    return {
        "case_id": case_id,

        "evidence_id": evidence_id,

        "name": path.name,

        "path": str(
            path.resolve()
        ),

        "extension": (
            path.suffix.lower()
            if path.suffix
            else "none"
        ),

        "size": stat.st_size,

        "created": datetime.fromtimestamp(
            stat.st_ctime
        ),

        "modified": datetime.fromtimestamp(
            stat.st_mtime
        ),

        "accessed": datetime.fromtimestamp(
            stat.st_atime
        ),

        "md5": hashes["md5"],

        "sha1": hashes["sha1"],

        "sha256": hashes["sha256"],

        "sha512": hashes["sha512"],
    }


def analyze_directory(
    directory,
    case_id,
    evidence_id
):

    directory = Path(directory)

    results = []

    for path in directory.rglob("*"):

        if not path.is_file():
            continue

        try:

            result = analyze_file(
                path,
                case_id,
                evidence_id
            )

            results.append(result)

        except (
            PermissionError,
            OSError
        ):
            continue

    return results