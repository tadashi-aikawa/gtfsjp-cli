#!/usr/bin/env python

import os

from owlmixin.util import load_csvf
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from gtfscli.dao.entities import (CONNECTION_STRING, Base, StopEntity, StopTimeEntity)
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
    base: str
    encoding: str
    session: Session

    stop: StopDao

    def insert_records(self, clz, file_name: str):
        # スピード優先でcoreを使う
        self.session.execute(
            clz.__table__.insert(),
            load_csvf(os.path.join(self.base, file_name), fieldnames=None, encoding=self.encoding)
        )

    def insert_tables(self):
        for e in ENTITIES:
            self.insert_records(e["clz"], e["file"])
        self.session.commit()

    def __init__(self, base: str, encoding: str):
        self.base = base
        self.encoding = encoding
        engine = create_engine(CONNECTION_STRING, echo=False)
        self.session: Session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)
        self.insert_tables()

        self.stop = StopDao(self.session)
