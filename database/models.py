from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_PATH


Base = declarative_base()


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True)

    case_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        default=""
    )

    investigator = Column(
        String(255),
        default=""
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True)

    evidence_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    case_id = Column(
        String(100),
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    path = Column(
        Text,
        nullable=False
    )

    size = Column(
        Integer,
        default=0
    )

    md5 = Column(
        String(32)
    )

    sha1 = Column(
        String(40)
    )

    sha256 = Column(
        String(64)
    )

    sha512 = Column(
        String(128)
    )

    added_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)

    case_id = Column(
        String(100),
        nullable=False
    )

    evidence_id = Column(
        String(100),
        nullable=False
    )

    name = Column(String(255))

    path = Column(Text)

    extension = Column(String(50))

    size = Column(Integer)

    created = Column(DateTime)

    modified = Column(DateTime)

    accessed = Column(DateTime)

    md5 = Column(String(32))

    sha1 = Column(String(40))

    sha256 = Column(String(64))

    sha512 = Column(String(128))


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True)

    case_id = Column(String(100))

    evidence_id = Column(String(100))

    timestamp = Column(DateTime)

    event_type = Column(String(100))

    source = Column(String(100))

    description = Column(Text)


engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)