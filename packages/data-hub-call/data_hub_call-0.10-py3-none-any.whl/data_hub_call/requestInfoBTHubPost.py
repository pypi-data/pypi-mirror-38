from requestInfoBTHub import RequestInfoBTHub, Feed_type, Request_type


class RequestInfoBTHubPost(RequestInfoBTHub):
    """A data stream from the restufl BT Data Hub style

    Attributes:
        api_core_url: The url of the data hub. eg 'http://api.bt-hypercat.com'
        feed_id: The id of the parent feed to which the datastream belongs
        datastream_id: the id of the datastream. Eg. 0, 1, 2...
        feed_type: either 'sensors', 'events', 'locations' or 'geo'
    """

    def __init__(self, api_key, username, api_core_url, feed_type, feed_id, datastream_id,
                 request_type, users_feed_name):
        super(RequestInfoBTHubPost, self).__init__(     api_key,
                                                        username,
                                                        api_core_url,
                                                        feed_type,
                                                        feed_id,
                                                        datastream_id,
                                                        request_type,
                                                        users_feed_name)


    def url_string(self):
        result = self.api_core_url + '/' + Feed_type(self.feed_type).name \
                 + '/feeds/' + self.feed_id

        if(self.datastream_id > -1):
            result += "/" + str(self.datastream_id)
        if(Request_type(self.request_type).value > 0):
            result += "/" + self.request_type.name

        return result


