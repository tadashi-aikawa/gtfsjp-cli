#!/usr/bin/env python

from owlmixin import OwlMixin, TList, TOption


class Agency(OwlMixin):
    id: str
    name: str
    zip_number: TOption[str]
    president_name: TOption[str]


class Stop(OwlMixin):
    id: str
    name: str
    kana: str
    en_name: TOption[str]
    trip_ids: TOption[TList[str]]


class GtfsClient:
    def __init__(self):
        raise NotImplementedError()

    def drop_and_create(
        self, gtfs_dir: str, *, encoding: str = "utf_8_sig", drop_duplicates: bool = False
    ):
        raise NotImplementedError()

    def find_stop_by_id(self, id_: str, with_trips: bool) -> TOption[Stop]:
        raise NotImplementedError()

    def search_stops_by_name(self, name: str, with_trips: bool) -> TList[Stop]:
        raise NotImplementedError()

    def fetch_agencies(self) -> TList[Agency]:
        raise NotImplementedError()
