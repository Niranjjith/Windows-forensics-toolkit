import hashlib

from modules.file_analyzer import calculate_hash


def test_sha256():

    test_file = "tests/test_file.txt"

    with open(
        test_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("forensics test")


    expected = hashlib.sha256(
        b"forensics test"
    ).hexdigest()

    actual = calculate_hash(
        test_file,
        "sha256"
    )

    assert actual == expected