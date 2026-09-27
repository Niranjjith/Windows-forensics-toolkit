from pathlib import Path
from uuid import uuid4

from sqlalchemy import select

from database.models import Evidence, SessionLocal
from core.hash_engine import calculate_all_hashes


def add_evidence(case_id, evidence_path):
    """
    Register an evidence file and calculate its forensic hashes.
    """

    path = Path(evidence_path).resolve()

    if not path.exists():
        raise FileNotFoundError(
            f"Evidence does not exist: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Evidence must be a file: {path}"
        )

    evidence_id = (
        "EVD-" + uuid4().hex[:8].upper()
    )

    hashes = calculate_all_hashes(path)

    evidence = Evidence(
        evidence_id=evidence_id,
        case_id=case_id,
        name=path.name,
        path=str(path),
        size=path.stat().st_size,
        md5=hashes["md5"],
        sha1=hashes["sha1"],
        sha256=hashes["sha256"],
        sha512=hashes["sha512"],
    )

    session = SessionLocal()

    try:
        session.add(evidence)
        session.commit()
        session.refresh(evidence)

        return evidence

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def get_evidence(case_id):
    """
    Return all evidence registered for a case.
    """

    session = SessionLocal()

    try:
        return session.scalars(
            select(Evidence).where(
                Evidence.case_id == case_id
            )
        ).all()

    finally:
        session.close()


def get_evidence_by_id(evidence_id):
    """
    Return a specific evidence record.
    """

    session = SessionLocal()

    try:
        return session.scalar(
            select(Evidence).where(
                Evidence.evidence_id == evidence_id
            )
        )

    finally:
        session.close()


def verify_evidence_exists(
    case_id,
    evidence_id
):
    """
    Check whether evidence belongs to a case.
    """

    session = SessionLocal()

    try:
        evidence = session.scalar(
            select(Evidence).where(
                Evidence.case_id == case_id,
                Evidence.evidence_id == evidence_id
            )
        )

        return evidence is not None

    finally:
        session.close()