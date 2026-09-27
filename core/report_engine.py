import json
from pathlib import Path
from datetime import datetime

from config import GENERATED_REPORTS_DIR


def generate_json_report(
    case_id,
    results
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output = (
        GENERATED_REPORTS_DIR
        / f"{case_id}_{timestamp}.json"
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            default=str
        )

    return output