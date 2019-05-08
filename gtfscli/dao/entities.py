#!/usr/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

CONNECTION_STRING = 'sqlite:///:memory:'
Base = declarative_base()


class StopEntity(Base):
    __tablename__ = 'stops'

    stop_id: str = Column(String, primary_key=True)
    stop_code: str = Column(String)
    stop_name: str = Column(String, nullable=False)
    stop_desc: str = Column(String)
    stop_lat: str = Column(String, nullable=False)
    stop_lon: str = Column(String, nullable=False)
    zone_id: str = Column(String)
    stop_url: str = Column(String)
    location_type: int = Column(Integer)
    parent_station: str = Column(String)
    stop_timezone: str = Column(String)
    wheelchair_boarding: int = Column(Integer)

    stop_times = relationship("StopTimeEntity", backref="stops")


class StopTimeEntity(Base):
    __tablename__ = 'stop_times'

    trip_id: str = Column(String, nullable=False, primary_key=True)
    arrival_time: str = Column(String, nullable=False)
    departure_time: str = Column(String, nullable=False)
    stop_id: str = Column(String, ForeignKey("stops.stop_id"), nullable=False)
    stop_sequence: int = Column(Integer, nullable=False, primary_key=True)
    stop_headsign: str = Column(String)
    pickup_type: int = Column(Integer)
    drop_off_type: int = Column(Integer)
    shape_dist_traveled: str = Column(String)
    timepoint: int = Column(Integer)

    stop = relationship("StopEntity")
