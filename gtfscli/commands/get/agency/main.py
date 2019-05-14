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

from gtfscli.services.agency import fetch_agencies


class Args(OwlMixin):
    source: str = "gtfs-jp.sqlite3"


def run(args: Args):
    print(fetch_agencies(args.source).to_pretty_json())
