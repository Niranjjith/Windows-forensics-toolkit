from pathlib import Path


BROWSER_DATABASES = [
    "History",
    "Cookies",
    "Web Data",
    "Login Data",
]


def find_browser_artifacts(path):

    path = Path(path)

    return [
        file
        for file in path.rglob("*")
        if file.is_file()
        and file.name in BROWSER_DATABASES
    ]