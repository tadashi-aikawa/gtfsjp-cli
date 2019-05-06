"""Get data related to stops

Usage:
  {cli} --id <id> <dir>
  {cli} (-h | --help)

Options:
  --id <id>                         Stop id
  <dir>                             GTFS dir
  -h --help                         Show this screen.
"""
from owlmixin import OwlMixin
from gtfscli.client.gtfs import GtfsClient


class Args(OwlMixin):
    id: str
    dir: str


def run(args: Args):
    print(
        GtfsClient(args.dir)\
          .find_stop_by_id(args.id)\
          .map(lambda x: x.to_yaml())\
          .get_or(f"Not found id = {args.id}")
    )
