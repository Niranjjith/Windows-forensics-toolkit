from database.models import Base, engine


def initialize_database():
    """
    Create all database tables.
    """

    Base.metadata.create_all(
        bind=engine
    )