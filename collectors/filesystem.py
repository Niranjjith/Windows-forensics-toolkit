from pathlib import Path


def discover_files(path):

    path = Path(path)

    if path.is_file():
        return [path]

    if path.is_dir():
        return [
            item
            for item in path.rglob("*")
            if item.is_file()
        ]

    raise FileNotFoundError(
        f"Path does not exist: {path}"
    )