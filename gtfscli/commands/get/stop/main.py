"""Get data related to stops

Usage:
  {cli} --id <id> <dir>
  {cli} (-w <word> | --word <word>) <dir>
  {cli} (-h | --help)

Options:
  --id <id>                         Stop id
  -w, --word <word>                 Search word for stop name
  <dir>                             GTFS dir
  -h --help                         Show this screen.
"""
from owlmixin import OwlMixin, TOption
from gtfscli.client.gtfs import GtfsClient


class Args(OwlMixin):
    id: TOption[str]
    word: TOption[str]
    dir: str


def search_by_id(gtfs_dir: str, id_: str) -> str:
    return GtfsClient(gtfs_dir).find_stop_by_id(id_)\
      .map(lambda x: x.to_yaml())\
      .get_or(f"Not found id = {id_}")


def search_by_word(gtfs_dir: str, word: str) -> str:
    return GtfsClient(gtfs_dir).search_stops_by_name(word).to_yaml()


def run(args: Args):
    args.id.map(lambda x: print(search_by_id(args.dir, x)))
    args.word.map(lambda x: print(search_by_word(args.dir, x)))
