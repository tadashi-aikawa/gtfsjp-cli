"""停留所/標柱情報の取得

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

from gtfscli.services.stop import search_by_word, search_by_id


class Args(OwlMixin):
    id: TOption[str]
    word: TOption[str]
    source: str = "gtfs-jp.sqlite3"


def run(args: Args):
    print(
        args.id.map(lambda id_: search_by_id(args.source, id_).to_pretty_json()).get()
        or args.word.map(lambda word: search_by_word(args.source, word).to_pretty_json()).get()
        or "到達しない領域に到達しました。実装に問題があります"
    )
