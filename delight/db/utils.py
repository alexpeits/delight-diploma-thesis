"""
Database helper utilities
~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from sqlalchemy import create_engine

from delight.config import DBConfig
from delight.db.models import Base


def create_tables():
    """Creates the database tables.

    This only has to be run once, and can be
    run with the command line tool:
        ./manage.py initdb
    """
    engine = create_engine(DBConfig.DB_URI)
    Base.metadata.create_all(engine)
