#!/usr/bin/env python

from typing import Iterable

from owlmixin import OwlMixin, TList, TOption

from gtfscli.client.db import DbClient
from gtfscli.dao.entities import StopEntity


class Stop(OwlMixin):
    id: str
    name: str
    times: TList[str]

    @classmethod
    def from_db_record(cls, record: StopEntity) -> 'TOption[Stop]':
        return Stop.from_dict({
            "id": record.stop_id,
            "name": record.stop_name,
            "times": [x.departure_time for x in record.stop_times]
        })

    @classmethod
    def from_db_records(cls, records: Iterable[StopEntity]) -> 'TList[Stop]':
        return TList(records).map(cls.from_db_record)


class GtfsClient():
    db: DbClient

    def __init__(self, gtfsdir: str, encoding: str = "utf_8_sig"):
        self.db: DbClient = DbClient(gtfsdir, encoding)

    def find_stop_by_id(self, id_: str) -> TOption[Stop]:
        return TOption(self.db.stop.find_by_id(id_)).map(Stop.from_db_record)

    def search_stops_by_name(self, name: str) -> TList[Stop]:
        return Stop.from_db_records(self.db.stop.search_by_name(name))