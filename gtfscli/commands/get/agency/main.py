"""事業者情報(詳細含む)の取得

Usage:
  {cli} [<source>]
  {cli} (-h | --help)

Options:
  <source>               GTFSソースのpath [default: gtfs-jp.sqlite3]
  -h --help              Show this screen.

Examples:
  {cli} tmp.sqlite3
"""
from owlmixin import OwlMixin
from gtfscli.client.gtfs import GtfsClient


class Args(OwlMixin):
    source: str = "gtfs-jp.sqlite3"


def fetch_agencies(source: str) -> str:
    return GtfsClient(source)\
        .fetch_agencies()\
        .map(lambda x: x.str_format("{id}: {name} (代表者: {president_name})"))\
        .join("\n")


def run(args: Args):
    print(fetch_agencies(args.source))
