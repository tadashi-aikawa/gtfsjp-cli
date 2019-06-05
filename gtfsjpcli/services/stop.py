from owlmixin import OwlMixin, TList, TIterator

from gtfsjpcli.client.factory import create_gtfs_client
from gtfsjpcli.client.gtfs import Stop


class StopDocument(OwlMixin):
    count: int
    stops: TList[Stop]


def search_by_id(source: str, id_: str) -> StopDocument:
    stop = create_gtfs_client(source).find_stop_by_id(id_)
    return StopDocument.from_dict(
        {"count": 1 if stop.any() else 0, "stops": stop.map(lambda x: [x]).get_or([])}
    )


def search_by_word(source: str, word: str) -> StopDocument:
    stops = create_gtfs_client(source).search_stops_by_name(word).to_list()
    return StopDocument.from_dict({"count": stops.size(), "stops": stops})
