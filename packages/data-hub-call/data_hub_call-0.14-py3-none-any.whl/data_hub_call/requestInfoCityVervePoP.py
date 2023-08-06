from data_hub_call.requestInfo import RequestInfo
from enum import Enum

class Element_type(Enum):
    __order__ = 'none entity'
    none = 0
    entity = 1

class RequestInfoCityVervePoP(RequestInfo):
    """A data stream from any restful CDP style platform/hub:
    """

    @staticmethod
    def get_element_types():
        return [(e.value, e.name) for e in Element_type]

    """Attributes:
        api_core_url: The url of the data hub. eg 'http://api.bt-hypercat.com'
        feed_id: The id of the parent feed to which the datastream belongs
        datastream_id: the id of the datastream. Eg. 0, 1, 2...
        feed_type: either 'sensors', 'events', 'locations' or 'geo'
    """

    HUB_ID = 'CDP'
    HUB_CALL_CLASSNAME = 'DataHubCallCityVervePoP'

    def __init__(self, api_key, api_core_url, request_type, sub_cat_name, stream_id,
                 users_feed_name, feed_info):
        super(RequestInfoCityVervePoP, self).__init__(api_core_url, users_feed_name, feed_info,
                                                       self.HUB_ID, self.HUB_CALL_CLASSNAME)

        self.api_key = api_key                  # https://api.cityverve.org.uk/v1
        self.request_type = request_type        # entity
        self.sub_cat_name = sub_cat_name        # air-quality-no2
        self.stream_id = stream_id              # 5db42367b00845dc44092a8b0dbe9892





