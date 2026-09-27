from datetime import datetime

from sqlalchemy import select

from database.models import Case, SessionLocal


def create_case(
    case_id: str,
    name: str,
    description: str = "",
    investigator: str = "",
):
    """
    Create and save a new forensic case.
    Returns a normal Python dictionary.
    """

    session = SessionLocal()

    try:
        existing = session.scalar(
            select(Case).where(
                Case.case_id == case_id
            )
        )

        if existing:
            raise ValueError(
                f"Case already exists: {case_id}"
            )

        case = Case(
            case_id=case_id,
            name=name,
            description=description,
            investigator=investigator,
            created_at=datetime.utcnow(),
        )

        session.add(case)
        session.commit()

        # Refresh while session is still active
        session.refresh(case)

        # Return plain Python data
        result = {
            "case_id": case.case_id,
            "name": case.name,
            "description": case.description,
            "investigator": case.investigator,
            "created_at": case.created_at,
        }

        return result

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def get_case(case_id: str):
    """
    Get one forensic case.
    Returns a dictionary or None.
    """

    session = SessionLocal()

    try:
        case = session.scalar(
            select(Case).where(
                Case.case_id == case_id
            )
        )

        if case is None:
            return None

        return {
            "case_id": case.case_id,
            "name": case.name,
            "description": case.description,
            "investigator": case.investigator,
            "created_at": case.created_at,
        }

    finally:
        session.close()


def list_cases():
    """
    Return all forensic cases.
    """

    session = SessionLocal()

    try:
        cases = session.scalars(
            select(Case).order_by(
                Case.created_at.desc()
            )
        ).all()

        return [
            {
                "case_id": case.case_id,
                "name": case.name,
                "description": case.description,
                "investigator": case.investigator,
                "created_at": case.created_at,
            }
            for case in cases
        ]

    finally:
        session.close()