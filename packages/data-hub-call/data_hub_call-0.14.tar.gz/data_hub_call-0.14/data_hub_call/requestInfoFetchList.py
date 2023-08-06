from data_hub_call.requestInfoList import RequestInfoList
from data_hub_call.requestInfoFetchFactory import RequestInfoFetchFactory
from enum import Enum

import json

class Data_request_type(Enum):
    feed_metadata = 1
    stream_metadata = 2
    data = 3


class RequestInfoFetchList(RequestInfoList):
    """A data stream from any platform/hub:
    """

    def __init__(self):
        super(RequestInfoFetchList, self).__init__()

    def clear_all(self):
        self.requests = []

    def append_request(self, hub_short_title, request_params, api_key=None, username=None):
        self.append(RequestInfoFetchFactory.create_request_info_fetch(hub_short_title, request_params, username, api_key))


    def append(self, request_info):
        self.requests.append(request_info)

    def get_list_of_users_stream_ids(self):
        result = []

        for request in self.requests:
            result.append(request.users_feed_name)

        return result









