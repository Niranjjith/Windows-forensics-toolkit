from pathlib import Path


def find_evtx_files(path):

    path = Path(path)

    if not path.exists():
        return []

    return [
        file
        for file in path.rglob("*.evtx")
        if file.is_file()
    ]