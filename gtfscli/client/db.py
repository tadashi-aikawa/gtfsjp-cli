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

    def insert_all(self):
        for e in ENTITIES:
            self.session.add_all([
                e["clz"](**x)
                for x in load_csvf(os.path.join(self.base, e['file']), fieldnames=None, encoding=self.encoding)
            ])

    def __init__(self, base: str, encoding: str):
        self.base = base
        self.encoding = encoding
        engine = create_engine(CONNECTION_STRING, echo=False)
        self.session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)
        self.insert_all()

        self.stop = StopDao(self.session)
