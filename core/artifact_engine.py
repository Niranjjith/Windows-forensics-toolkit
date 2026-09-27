from analyzers.file_analyzer import (
    analyze_directory
)


def collect_filesystem_artifacts(
    path,
    case_id,
    evidence_id
):

    return analyze_directory(
        path,
        case_id,
        evidence_id
    )