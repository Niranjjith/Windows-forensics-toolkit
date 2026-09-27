from pathlib import Path

from analyzers.file_analyzer import (
    analyze_directory
)


def generate_file_timeline(
    path,
    case_id,
    evidence_id
):

    files = analyze_directory(
        path,
        case_id,
        evidence_id
    )

    events = []

    for file in files:

        events.append({
            "timestamp": file["created"],
            "event_type": "CREATED",
            "source": "FILESYSTEM",
            "description": file["path"]
        })

        events.append({
            "timestamp": file["modified"],
            "event_type": "MODIFIED",
            "source": "FILESYSTEM",
            "description": file["path"]
        })

        events.append({
            "timestamp": file["accessed"],
            "event_type": "ACCESSED",
            "source": "FILESYSTEM",
            "description": file["path"]
        })

    return sorted(
        events,
        key=lambda event: event["timestamp"]
    )