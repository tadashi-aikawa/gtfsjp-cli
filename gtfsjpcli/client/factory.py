#!/usr/bin/env python

from gtfsjpcli.client.gtfs import GtfsClient
from gtfsjpcli.client.gtfsdb import GtfsDbClient


def create_gtfs_client(source: str) -> GtfsClient:
    return GtfsDbClient(source)
