"""GTFSデータからデータベースを作成します

Usage:
  {cli} <gtfs_dir> [-d | --drop-duplicates] [<dst>]
  {cli} (-h | --help)

Options:
  <gtfs_dir>                        GTFSディレクトリ
  -d --drop-duplicates              完全一致するレコードを削除する
  <dst>                             DB作成先 [default: gtfs-jp.sqlite3]
  -h --help                         Show this screen.

Examples:
  {cli} C:\\Users\\gtfs\\Donanbus
  {cli} C:\\Users\\gtfs\\Donanbus -d tmp.sqlite3
"""
from owlmixin import OwlMixin
from gtfscli.client.gtfs import GtfsClient


class Args(OwlMixin):
    gtfs_dir: str
    drop_duplicates: bool
    dst: str = "gtfs-jp.sqlite3"


def run(args: Args):
    GtfsClient(args.dst).drop_and_create(args.gtfs_dir, drop_duplicates=args.drop_duplicates)
