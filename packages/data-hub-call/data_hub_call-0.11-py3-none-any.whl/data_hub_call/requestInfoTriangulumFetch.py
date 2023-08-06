from data_hub_call.requestInfoTriangulum import RequestInfoTriangulum, Feed_type_pi, Request_type_pi
import json

class RequestInfoTriangulumFetch(RequestInfoTriangulum):
    """A data stream from any hypercat platform/hub:
    """

    def __init__(self, params, metadata=False):
        try:
            json_params = json.loads(params)
            self.init_json(json_params)
        except:
            try:
                json_params_str = json.dumps(params)
                self.init_json(params)
            except:
                try:
                    self.init_csv(params, metadata)
                except Exception as err:
                    raise err

    class Factory:
        def create(self, username, api_key, params):
            return RequestInfoTriangulumFetch(params)




    def init_json(self, params, metadata=False):
        # https://130.88.97.137/piwebapi,streams,A0EXpbRmwnc7kq0OSy1LydJJQxey0y1BT5hGA3gBQVqtCQgLR6A7xNbjk6RXQ6dns2
        # VqAVk0tUEktUDAxLkRTLk1BTi5BQy5VS1xUUklBTkdVTFVNXEFJUiBRVUFMSVRZXE9YRk9SRCBST0FEfE5PIExFVkVM,
        # interpolated,Anns_Pi_feed_Nitrogen
        core_url_string = params['stream_params'][0]
        host = core_url_string.replace('https://', '').replace('http://', '').replace('/piwebapi', '')
        stream_params = params['stream_params'][2]
        if (metadata):
            feed_type = Feed_type_pi.attributes
            request_type = Request_type_pi.none
        else:
            feed_type = Feed_type_pi[params['stream_params'][1]]
            if len(params['stream_params']) > 3:
                request_type = Request_type_pi[params['stream_params'][3].rstrip('\n')]
            else:
                request_type = Request_type_pi.none
        try:
            users_feed_name = params['user_defined_name'].rstrip('\n')
        except:
            users_feed_name = ''

        if 'feed_info' in params:
            feed_info = params['feed_info']
        else:
            feed_info = {}

        try:
            super(RequestInfoTriangulumFetch, self).__init__(host,
                                                                core_url_string,
                                                                feed_type,
                                                                stream_params,
                                                                request_type,
                                                                users_feed_name,
                                                                feed_info)
        except:
            raise ValueError("Error creating new request (triangulum): " + json.dumps(params))

    def init_csv(self, params, metadata=False):
        list_params = params.split(",")
        # https://130.88.97.137/piwebapi,streams,A0EXpbRmwnc7kq0OSy1LydJJQxey0y1BT5hGA3gBQVqtCQgLR6A7xNbjk6RXQ6dns2
        # VqAVk0tUEktUDAxLkRTLk1BTi5BQy5VS1xUUklBTkdVTFVNXEFJUiBRVUFMSVRZXE9YRk9SRCBST0FEfE5PIExFVkVM,
        # interpolated,Anns_Pi_feed_Nitrogen
        core_url_string = list_params[0]
        host = core_url_string.replace('https://', '').replace('http://', '').replace('/piwebapi', '')
        param_list = list_params[2]
        if (metadata):
            feed_type = Feed_type_pi.attributes
            request_type = Request_type_pi.none
        else:
            feed_type = Feed_type_pi[list_params[1]]
            request_type = Request_type_pi[list_params[3].rstrip('\n')]
        try:
            users_feed_name = list_params[4].rstrip('\n')
        except:
            users_feed_name = ''

        if (len(list_params) > 5):
            str_feed_info = ','.join(list_params[5:])
            feed_info = json.loads(str_feed_info)
        else:
            feed_info = {}

        try:
            super(RequestInfoTriangulumFetch, self).__init__(host,
                                                                core_url_string,
                                                                feed_type,
                                                                param_list,
                                                                request_type,
                                                                users_feed_name,
                                                                feed_info)
        except:
            raise ValueError("Error creating new request (triangulum): " + params)



    def url_string(self):
        result = self.api_core_url

        if(Feed_type_pi(self.feed_type).value > 0):
            result +=  '/' + Feed_type_pi(self.feed_type).name
        if(len(self.params) > 0):
            result += '/' + self.params
        if (Request_type_pi(self.request_type).value > 0):
            result += "/" + Request_type_pi(self.request_type).name
        return result


    def csv_line_string(self, includeUsersName=True, includesFeedInfo=True):
        # https://130.88.97.137/piwebapi,streams/
        # A0EXpbRmwnc7kq0OSy1LydJJQxey0y1BT5hGA3gBQVqtCQgLR6A7xNbjk6RXQ6dns2VqAVk0tUEktUDAxLkRTLk1BTi5BQy5VS1x
        # UUklBTkdVTFVNXEFJUiBRVUFMSVRZXE9YRk9SRCBST0FEfE5PIExFVkVM/interpolated,Anns_Pi_feed_Nitrogen

        result = self.api_core_url
        result += ',' + Feed_type_pi(self.feed_type).name
        result += ',' + self.params
        result += "," + self.request_type.name
        if(includeUsersName):
            result += "," + self.users_feed_name
        if (includesFeedInfo):
            result += "," + json.dumps(self.feed_info)

        return result

