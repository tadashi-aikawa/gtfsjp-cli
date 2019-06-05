from owlmixin import OwlMixin, TList

from gtfsjpcli.client.factory import create_gtfs_client
from gtfsjpcli.client.gtfs import Agency


class AgencyDocument(OwlMixin):
    count: int
    agencies: TList[Agency]


def fetch_agencies(source: str) -> TList[AgencyDocument]:
    agencies = create_gtfs_client(source).fetch_agencies()
    return AgencyDocument.from_dict({"count": agencies.size(), "agencies": agencies})
