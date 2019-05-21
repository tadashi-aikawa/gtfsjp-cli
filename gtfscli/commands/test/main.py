"""動作確認用コマンド

Usage:
  {cli} <something>
  {cli} (-h | --help)

Options:
  -h --help                         Show this screen.

Examples:
  {cli}
"""

from owlmixin import OwlMixin, TList

from gtfscli.client.gtfsdb import GtfsDbClient
from gtfscli.dao.entities import FareRuleEntity


class Args(OwlMixin):
    something: str


def to_record(x: FareRuleEntity) -> dict:
    return {"fromノード": x.origin_stop.stop_name, "toノード": x.destination_stop.stop_name, "運賃": x.fare_attribute.price}


def run(args: Args):
    route = GtfsDbClient("gtfs-jp.sqlite3").route.find_by_id("20002_200243_1")

    print(
        f"""
------------------------------------------------------------------------
| 系統ID: {route.route_id}
| 系統名: {route.route_short_name}
------------------------------------------------------------------------
{TList(map(to_record, route.fare_rules)).to_table(["fromノード", "toノード", "運賃"])}
"""
    )
