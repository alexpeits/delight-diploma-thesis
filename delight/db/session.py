"""
Database session creation
~~~~~~~~~~~~~~~~~~~~~~~~~

This module exports the sqlalchemy `session` object

"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from delight.config import DBConfig
from delight.db.models import Base


_engine = create_engine(DBConfig.DB_URI)
Base.metadata.bind = _engine

_db_session = sessionmaker(bind=_engine)

session = _db_session()
