#!/usr/bin/env python

from gtfscli.client.gtfs import GtfsClient
from gtfscli.client.gtfsdb import GtfsDbClient


def create_gtfs_client(source: str) -> GtfsClient:
    return GtfsDbClient(source)
