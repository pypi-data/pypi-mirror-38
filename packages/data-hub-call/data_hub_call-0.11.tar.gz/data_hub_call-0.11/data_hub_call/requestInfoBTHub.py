from data_hub_call.requestInfo import RequestInfo
from enum import Enum


class Feed_type(Enum):
    __order__ = 'events locations sensors sensors2 journeys'
    events = 1
    locations = 2
    sensors = 3
    sensors2 = 4
    journeys = 5

class Request_type(Enum):
    __order__ = 'none datapoints events'
    none = 0
    datapoints = 1
    events = 2

class RequestInfoBTHub(RequestInfo):
    """A data stream from any restful BT style platform/hub:
    """

    @staticmethod
    def get_feed_types():
        return [(e.value, e.name) for e in Feed_type]

    @staticmethod
    def get_request_types():
        return [(e.value, e.name) for e in Request_type]

    """Attributes:
        api_core_url: The url of the data hub. eg 'http://api.bt-hypercat.com'
        feed_id: The id of the parent feed to which the datastream belongs
        datastream_id: the id of the datastream. Eg. 0, 1, 2...
        feed_type: either 'sensors', 'events', 'locations' or 'geo'
    """

    HUB_ID = 'BT'
    HUB_CALL_CLASSNAME = 'DataHubCallBTHub'

    def __init__(self, api_key, username, api_core_url, feed_type, feed_id, datastream_id,
                 request_type, users_feed_name, feed_info):

        super(RequestInfoBTHub, self).__init__(api_core_url, users_feed_name, feed_info,
                                                      self.HUB_ID, self.HUB_CALL_CLASSNAME)

        self.api_key = api_key
        self.username = username
        self.feed_type = feed_type
        self.feed_id = feed_id
        self.datastream_id = datastream_id
        self.request_type = request_type




