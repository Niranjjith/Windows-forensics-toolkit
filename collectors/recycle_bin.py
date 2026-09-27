from pathlib import Path


def find_recycle_bin_files(path):

    path = Path(path)

    return [
        file
        for file in path.rglob("$I*")
        if file.is_file()
    ]