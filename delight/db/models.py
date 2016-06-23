"""
Database models
~~~~~~~~~~~~~~~

Declarations of database models for storing
power measurements. Used by the gui for displaying
historical power consumption data

"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func


Base = declarative_base()


class PowerMeasurement(Base):
    """Power dissipation measurements."""

    __tablename__ = 'power_measurements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, nullable=False)
    measurement = Column(Float, nullable=False)
    datetime = Column(DateTime(timezone=True), server_default=func.now())
