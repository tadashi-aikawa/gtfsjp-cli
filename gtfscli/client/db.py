#!/usr/bin/env python

import csv
import json
import os
from typing import List, Optional, Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from gtfscli.dao.agency import AgencyDao
from gtfscli.dao.entities import (
    Base, StopEntity, StopTimeEntity, AgencyEntity, AgencyJpEntity, CalendarEntity, RouteEntity, RouteJpEntity,
    TripEntity, OfficeJpEntity, FareRuleEntity, FareAttributeEntity, CalendarDateEntity, ShapeEntity, FeedInfoEntity,
    TranslationEntity
)
from gtfscli.dao.stop import StopDao

ENTITIES = [
    {
        "file": "agency.txt",
        "clz": AgencyEntity
    },
    {
        "file": "agency_jp.txt",
        "clz": AgencyJpEntity
    },
    {
        "file": "routes.txt",
        "clz": RouteEntity
    },
    {
        "file": "routes_jp.txt",
        "clz": RouteJpEntity
    },
    {
        "file": "trips.txt",
        "clz": TripEntity
    },
    {
        "file": "office_jp.txt",
        "clz": OfficeJpEntity
    },
    {
        "file": "stops.txt",
        "clz": StopEntity
    },
    {
        "file": "stop_times.txt",
        "clz": StopTimeEntity
    },
    {
        "file": "calendar.txt",
        "clz": CalendarEntity
    },
    {
        "file": "calendar_dates.txt",
        "clz": CalendarDateEntity
    },
    {
        "file": "fare_attributes.txt",
        "clz": FareAttributeEntity
    },
    {
        "file": "fare_rules.txt",
        "clz": FareRuleEntity
    },
    {
        "file": "shapes.txt",
        "clz": ShapeEntity
    },
    {
        "file": "feed_info.txt",
        "clz": FeedInfoEntity
    },
    {
        "file": "translations.txt",
        "clz": TranslationEntity
    },
]


def load_csvf(fpath: str, fieldnames: Optional[List[str]], encoding: str = "utf-8",
              drop_duplicates: bool = False) -> Iterable[dict]:
    """CSVファイルを読み込みます

    Args:
        fpath: CSVファイルのパス
        fieldnames: カラム名 (Noneの場合はヘッダの値を使用します)
        encoding: エンコーディング
        drop_duplicates: 完全重複するレコードを削除するかどうか
    """
    with open(fpath, mode='r', encoding=encoding) as f:
        snippet = f.read(8192)
        f.seek(0)

        dialect = csv.Sniffer().sniff(snippet)
        dialect.skipinitialspace = True
        it = csv.DictReader(f, fieldnames=fieldnames, dialect=dialect)

        if not drop_duplicates:
            yield from it
        else:
            sorted_list = sorted(it, key=lambda x: json.dumps(x, ensure_ascii=False))
            previous: str = None
            for current in sorted_list:
                if drop_duplicates and current == previous:
                    continue
                yield current
                previous = current


class DbClient():
    engine: any
    session: Session

    stop: StopDao
    agency: AgencyDao

    def __init__(self, dbpath: str):
        connection_string = dbpath or ':memory:'
        self.engine = create_engine(f'sqlite:///{connection_string}', echo=False)
        self.session: Session = sessionmaker(bind=self.engine)()

        self.agency = AgencyDao(self.session)
        self.stop = StopDao(self.session)

    def create_database_with_inserts(self, gtfs_dir: str, encoding: str, drop_duplicates: bool):
        Base.metadata.create_all(self.engine)
        for e in [x for x in ENTITIES if os.path.exists(os.path.join(gtfs_dir, x["file"]))]:
            self.__insert_records(gtfs_dir, e["clz"], e["file"], encoding, drop_duplicates)
        self.session.commit()

    def drop_database(self):
        Base.metadata.drop_all(self.engine)

    def __insert_records(self, gtfs_dir: str, clz, file_name: str, encoding: str, drop_duplicates: bool):
        dicts = load_csvf(
            os.path.join(gtfs_dir, file_name), fieldnames=None, encoding=encoding, drop_duplicates=drop_duplicates
        )
        # スピード優先でcoreを使う
        self.session.execute(clz.__table__.insert(), list(dicts))
