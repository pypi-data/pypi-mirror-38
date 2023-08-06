# Polymorphic factory methods.
from __future__ import generators
from data_hub_call.requestInfoBTHubFetch import RequestInfoBTHubFetch
from data_hub_call.requestInfoCityVervePoPFetch import RequestInfoCityVervePoPFetch
from data_hub_call.requestInfoTriangulumFetch import RequestInfoTriangulumFetch


class RequestInfoFetchFactory:
    factories = {}

    def add_factory(id, request_info_factory):
        RequestInfoFetchFactory.factories.put[id] = request_info_factory
    add_factory = staticmethod(add_factory)

    # A Template Method:
    def create_request_info_fetch(hub_short_title, request_params, username, api_key):
        if hub_short_title not in RequestInfoFetchFactory.factories:
            RequestInfoFetchFactory.factories[hub_short_title] = eval('RequestInfo'
                                                                      + hub_short_title.replace("-", "")
                                                                      + 'Fetch'
                                                                      + '.Factory()')
        return RequestInfoFetchFactory.factories[hub_short_title].create(username, api_key, request_params)

    create_request_info_fetch = staticmethod(create_request_info_fetch)

