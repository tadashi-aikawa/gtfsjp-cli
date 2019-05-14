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
from owlmixin import OwlMixin, TList
from gtfscli.client.gtfs import GtfsClient, Agency


class Args(OwlMixin):
    source: str = "gtfs-jp.sqlite3"


def fetch_agencies(source: str) -> TList[Agency]:
    return GtfsClient(source).fetch_agencies()


def run(args: Args):
    agencies = fetch_agencies(args.source)
    print(
        f"""
事業者: {agencies[0].name}
〒: {agencies[0].zip_number.get_or("なし")}
代表者: {agencies[0].president_name.get_or("なし")}
"""
    )
