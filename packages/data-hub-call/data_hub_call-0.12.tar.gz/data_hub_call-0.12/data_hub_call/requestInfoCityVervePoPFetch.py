from data_hub_call.requestInfoCityVervePoP import RequestInfoCityVervePoP, Element_type
from enum import Enum
import json
from ast import literal_eval

#E.G.: https://api.cityverve.org.uk/v1/entity/noise-meter/6472W/timeseries/dose/datapoints

class Stream_type(Enum):
    __order__ = 'none timeseries static'
    none = 0
    timeseries = 1
    static = 2

class Request_type(Enum):
    __order__ = 'none entity cat'
    none = 0
    entity = 1
    cat = 2


class RequestInfoCityVervePoPFetch(RequestInfoCityVervePoP):
    """A data stream from the BT Data Hub

    """
    @staticmethod
    def get_stream_types():
        return [(e.value, e.name) for e in Stream_type]

    def __init__(self, api_key, params):
        try:
            json_params = json.loads(params)
            self.init_json(api_key, json_params)
        except:
            try:
                json_params_str = json.dumps(params)
                self.init_json(api_key, params)
            except:
                try:
                    self.init_csv(api_key, params)
                except Exception as err:
                    raise err

    class Factory:
        def create(self, username, api_key, params):
            return RequestInfoCityVervePoPFetch(api_key, params)


    def init_csv(self, api_key, params):
        # 'https://api.cityverve.org.uk/v1,entity,air-quality-no2,5db42367b00845dc44092a8b0dbe9892,'

        # import hypercat stream
        list_params = params.split(",")
        core_url_string = list_params[0]
        request_type = Request_type[list_params[1]]
        sub_cat_name = list_params[2]
        stream_id = list_params[3]

        try:
            params_list = literal_eval(list_params[4].rstrip('\n'))  # {'limit': '100'} '{\\'limit\\':\\'100\\'}'
        except:
            params_list = {}

        try:
            users_feed_name = list_params[5].rstrip('\n')
        except:
            users_feed_name = ''

        if (len(list_params) > 6):
            str_feed_info = ','.join(list_params[6:])
            feed_info = json.loads(str_feed_info)
        else:
            feed_info = {}

        try:
            super(RequestInfoCityVervePoPFetch, self).__init__(api_key,
                                                                core_url_string,
                                                                request_type,
                                                                sub_cat_name,
                                                                stream_id,
                                                                users_feed_name,
                                                                feed_info)
            self.params = params_list
        except:
            # raise;
            raise Exception("Error creating new request (cdp): " + params)


    def init_json(self, api_key, params):
        # {"feed_info": {"href": "https://api.cityverve.org.uk/v1/entity/crime", "time_field": "entity.occurred"},
        # "user_defined_name": "crimes",
        # "stream_params": ["https://api.cityverve.org.uk", "v1", "entity", "crime", "", "static", "", "datapoints","{}"]}

        list_params = params['stream_params']
        core_url_string = list_params[0]
        request_type = Request_type[list_params[1]]
        sub_cat_name = list_params[2]
        stream_id = list_params[3]

        try:
            params_list = literal_eval(list_params[4].rstrip('\n'))  # {'limit': '100'} '{\\'limit\\':\\'100\\'}'
        except:
            params_list = {}

        try:
            users_feed_name = params['user_defined_name'].rstrip('\n')
        except:
            users_feed_name = ''

        if 'feed_info' in params:
            feed_info = params['feed_info']
        else:
            feed_info = {}

        try:
            super(RequestInfoCityVervePoPFetch, self).__init__(api_key,
                                                                core_url_string,
                                                                request_type,
                                                                sub_cat_name,
                                                                stream_id,
                                                                users_feed_name,
                                                                feed_info)
            self.params = params_list  # API's allowed param list eg 'offset=12&limit=10'
        except:
            raise Exception("Error creating new request (CDP): " + json.dumps(params))


    def url_string(self):
        # 'https://api.cityverve.org.uk/v1,entity,air-quality-no2,5db42367b00845dc44092a8b0dbe9892,'
        result = self.api_core_url + '/' + Request_type(self.request_type).name
        if self.sub_cat_name.strip() != '':
            result += '/'+ self.sub_cat_name
            if self.stream_id.strip() != '':
                result += '/' + self.stream_id

        return result


    def user_defined_name(self):
        return self.users_feed_name