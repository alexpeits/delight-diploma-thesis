"""
Database helper utilities
~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from sqlalchemy import create_engine

from delight.config import DBConfig
from delight.db.models import Base


def create_tables():
    engine = create_engine(DBConfig.DB_URI)
    Base.metadata.create_all(engine)
