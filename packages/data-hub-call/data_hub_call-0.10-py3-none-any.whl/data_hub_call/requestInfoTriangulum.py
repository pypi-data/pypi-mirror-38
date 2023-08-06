from data_hub_call.requestInfo import RequestInfo
from enum import Enum

class Feed_type_pi(Enum):
    __order__ = 'none streams streamsets elements attributes assetdatabases points'
    none = 0
    streams = 1
    streamsets = 2
    elements = 3
    attributes = 4
    assetdatabases = 5
    points = 6

class Request_type_pi(Enum):
    __order__ = 'none plot interpolated summary recorded elements attributes value'
    none = 0
    plot = 1
    interpolated = 2
    summary = 3
    recorded = 4
    elements = 5
    attributes = 6
    value = 7


class RequestInfoTriangulum(RequestInfo):
    """A data stream from any hypercat platform/hub:
    """

    @staticmethod
    def get_feed_types():
        return [(e.value, e.name) for e in Feed_type_pi]

    @staticmethod
    def get_request_types():
        return [(e.value, e.name) for e in Request_type_pi]

    HUB_ID = 'Triangulum'
    HUB_CALL_CLASSNAME = 'DataHubCallTriangulum'

    def __init__(self, host, api_core_url, feed_type, params, request_type, users_feed_name, feed_info):

        super(RequestInfoTriangulum, self).__init__(api_core_url, users_feed_name, feed_info,
                                                      self.HUB_ID, self.HUB_CALL_CLASSNAME)

        self.host = host
        self.feed_type = feed_type
        self.params = params
        self.request_type = request_type









