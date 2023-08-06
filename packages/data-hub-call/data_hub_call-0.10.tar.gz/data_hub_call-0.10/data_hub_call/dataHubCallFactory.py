# Polymorphic factory methods.
from __future__ import generators
from data_hub_call.dataHubCallTriangulum import DataHubCallTriangulum
from data_hub_call.dataHubCallCityVervePoP import DataHubCallCityVervePoP
from data_hub_call.dataHubCallBTHub import DataHubCallBTHub

class DataHubCallFactory:
    factories = {}

    def add_factory(id, data_hub_call_factory):
        DataHubCallFactory.factories.put[id] = data_hub_call_factory
    add_factory = staticmethod(add_factory)

    # A Template Method:
    def create_data_hub_call(request):
        if request.hub_call_classname not in DataHubCallFactory.factories:
            DataHubCallFactory.factories[request.hub_call_classname] = eval(request.hub_call_classname + '.Factory()')
        return DataHubCallFactory.factories[request.hub_call_classname].create(request)

    create_data_hub_call = staticmethod(create_data_hub_call)