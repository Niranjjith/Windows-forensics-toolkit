import hashlib
from pathlib import Path


BUFFER_SIZE = 1024 * 1024


SUPPORTED_ALGORITHMS = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
]


def calculate_hash(
    file_path,
    algorithm="sha256"
):
    """
    Calculate a cryptographic hash for a file.
    """

    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm: {algorithm}"
        )

    path = Path(file_path)

    hash_object = hashlib.new(
        algorithm
    )

    with open(path, "rb") as file:

        while True:

            chunk = file.read(
                BUFFER_SIZE
            )

            if not chunk:
                break

            hash_object.update(chunk)

    return hash_object.hexdigest()


def calculate_all_hashes(file_path):
    """
    Calculate all supported hashes.
    """

    return {
        "md5": calculate_hash(
            file_path,
            "md5"
        ),

        "sha1": calculate_hash(
            file_path,
            "sha1"
        ),

        "sha256": calculate_hash(
            file_path,
            "sha256"
        ),

        "sha512": calculate_hash(
            file_path,
            "sha512"
        ),
    }


def verify_hash(
    file_path,
    expected_hash,
    algorithm="sha256"
):
    """
    Verify a file against an expected hash.
    """

    actual_hash = calculate_hash(
        file_path,
        algorithm
    )

    return (
        actual_hash.lower()
        == expected_hash.lower()
    )