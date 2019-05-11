"""GTFSデータからデータベースを作成します

Usage:
  {cli} <gtfs_dir> [<dst>]
  {cli} (-h | --help)

Options:
  <gtfs_dir>                        GTFSディレクトリ
  <dst>                             DB作成先 [default: gtfs-jp.sqlite3]
  -h --help                         Show this screen.

Examples:
  {cli} C:\\Users\\gtfs\\Donanbus
  {cli} C:\\Users\\gtfs\\Donanbus tmp.sqlite3
"""
from owlmixin import OwlMixin
from gtfscli.client.gtfs import GtfsClient


class Args(OwlMixin):
    gtfs_dir: str
    dst: str = "gtfs-jp.sqlite3"


def run(args: Args):
    GtfsClient(args.dst).drop_and_create(args.gtfs_dir)
