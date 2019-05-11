#!/usr/bin/env python

from typing import Iterable

from owlmixin import OwlMixin, TList, TOption

from gtfscli.client.db import DbClient
from gtfscli.dao.entities import StopEntity, AgencyEntity


class Agency(OwlMixin):
    id: str
    name: str
    zip_number: TOption[str]
    president_name: TOption[str]

    @classmethod
    def from_db_record(cls, record: AgencyEntity) -> 'Agency':
        return Agency.from_dict(
            {
                "id": record.agency_id,
                "name": record.agency_name,
                "zip_number": record.extra.agency_zip_number,
                "president_name": record.extra.agency_president_name,
            }
        )

    @classmethod
    def from_db_records(cls, records: Iterable[AgencyEntity]) -> 'TList[Agency]':
        return TList(records).map(cls.from_db_record)


class Stop(OwlMixin):
    id: str
    name: str
    times: TList[str]

    @classmethod
    def from_db_record(cls, record: StopEntity) -> 'Stop':
        return Stop.from_dict(
            {
                "id": record.stop_id,
                "name": record.stop_name,
                "times": [x.departure_time for x in record.stop_times]
            }
        )

    @classmethod
    def from_db_records(cls, records: Iterable[StopEntity]) -> 'TList[Stop]':
        return TList(records).map(cls.from_db_record)


class GtfsClient():
    db: DbClient

    def __init__(self, source: str = "gtfs-jp.sqlite3"):
        self.db: DbClient = DbClient(source)

    def drop_and_create(self, gtfs_dir: str, encoding: str = "utf_8_sig"):
        self.db.drop_database()
        self.db.create_database_with_inserts(gtfs_dir, encoding)

    def find_stop_by_id(self, id_: str) -> TOption[Stop]:
        return TOption(self.db.stop.find_by_id(id_)).map(Stop.from_db_record)

    def search_stops_by_name(self, name: str) -> TList[Stop]:
        return Stop.from_db_records(self.db.stop.search_by_name(name))

    def fetch_agencies(self) -> TList[Agency]:
        return Agency.from_db_records(self.db.agency.all())
