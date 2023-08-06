class RequestInfo(object):
    """A data stream from any platform/hub:
    """

    def __init__(self, api_core_url, users_feed_name, feed_info, hub_id, hub_call_classname):
        self.last_fetch_time = None

        self.api_core_url = api_core_url
        self.users_feed_name = users_feed_name
        self.feed_info = feed_info
        self.hub_id = hub_id
        self.hub_call_classname = hub_call_classname
