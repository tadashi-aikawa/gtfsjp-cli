"""Get data related to stops

Usage:
  {cli} --id <id> [<source>]
  {cli} (-w <word> | --word <word>) [<source>]
  {cli} (-h | --help)

Options:
  --id <id>              検索するStopのID
  -w, --word <word>      検索するStop名称(部分一致)
  <source>               GTFSソースのpath [default: gtfs-jp.sqlite3]
  -h --help              Show this screen.

Examples:
  {cli} --id C03_1
  {cli} -w 東京 tmp.sqlite3
"""
from owlmixin import OwlMixin, TOption
from gtfscli.client.gtfs import GtfsClient


class Args(OwlMixin):
    id: TOption[str]
    word: TOption[str]
    source: str = "gtfs-jp.sqlite3"


def search_by_id(source: str, id_: str) -> str:
    return GtfsClient(source).find_stop_by_id(id_)\
        .map(lambda x: f"[{x.id}]: {x.name}")\
        .get_or(f"Not found id = {id_}")


def search_by_word(source: str, word: str) -> str:
    return GtfsClient(source)\
        .search_stops_by_name(word)\
        .map(lambda x: x.str_format("{id}: {name}"))\
        .join("\n")


def run(args: Args):
    args.id.map(lambda x: print(search_by_id(args.source, x)))
    args.word.map(lambda x: print(search_by_word(args.source, x)))
