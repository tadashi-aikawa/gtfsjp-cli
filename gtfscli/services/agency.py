from owlmixin import OwlMixin, TList
from gtfscli.client.gtfs import GtfsClient, Agency


class AgencyDocument(OwlMixin):
    count: int
    agencies: TList[Agency]


def fetch_agencies(source: str) -> TList[AgencyDocument]:
    agencies = GtfsClient(source).fetch_agencies()
    return AgencyDocument.from_dict({"count": agencies.size(), "agencies": agencies})
