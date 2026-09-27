import logging
from pathlib import Path


LOG_DIRECTORY = Path("reports")
LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIRECTORY / "forensics.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)


logger = logging.getLogger(
    "windows_forensics_toolkit"
)