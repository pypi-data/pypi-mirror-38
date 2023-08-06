
class RequestInfoList(object):
    """A data stream from any platform/hub:
    """

    def __init__(self):
        self.requests = []


    def __len__(self):
        return len(self.requests)



