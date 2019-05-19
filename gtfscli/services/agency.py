from owlmixin import OwlMixin, TList

from gtfscli.client.gtfs import Agency
from gtfscli.client.gtfsdb import GtfsDbClient


class AgencyDocument(OwlMixin):
    count: int
    agencies: TList[Agency]


def fetch_agencies(source: str) -> TList[AgencyDocument]:
    agencies = GtfsDbClient(source).fetch_agencies()
    return AgencyDocument.from_dict({"count": agencies.size(), "agencies": agencies})
