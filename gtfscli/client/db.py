#!/usr/bin/env python

import os

from owlmixin.util import load_csvf
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from gtfscli.dao.entities import (Base, StopEntity, StopTimeEntity)
from gtfscli.dao.stop import StopDao

ENTITIES = [
    {
        "file": "stops.txt",
        "clz": StopEntity
    },
    {
        "file": "stop_times.txt",
        "clz": StopTimeEntity
    },
]


class DbClient():
    engine: any
    session: Session

    stop: StopDao

    def __init__(self, dbpath: str):
        connection_string = dbpath or ':memory:'
        self.engine = create_engine(f'sqlite:///{connection_string}', echo=False)
        self.session: Session = sessionmaker(bind=self.engine)()

        self.stop = StopDao(self.session)

    def create_database_with_inserts(self, gtfs_dir: str, encoding: str):
        Base.metadata.create_all(self.engine)
        for e in ENTITIES:
            self.__insert_records(gtfs_dir, e["clz"], e["file"], encoding)
        self.session.commit()

    def drop_database(self):
        Base.metadata.drop_all(self.engine)

    def __insert_records(self, gtfs_dir: str, clz, file_name: str, encoding: str):
        # スピード優先でcoreを使う
        self.session.execute(
            clz.__table__.insert(), load_csvf(os.path.join(gtfs_dir, file_name), fieldnames=None, encoding=encoding)
        )
