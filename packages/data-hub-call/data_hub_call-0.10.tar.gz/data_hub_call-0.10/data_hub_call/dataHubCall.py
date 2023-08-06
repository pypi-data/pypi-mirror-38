import datetime
import re
from dateutil.parser import parse
from abc import ABCMeta, abstractmethod



class DataHubCall(object):
    """A data hub call:
    """

    def __init__(self, core_url, request_info, hub_id):
        self. core_URL = core_url
        self.request_info = request_info
        self.hub_id = hub_id

    @abstractmethod
    def get_influx_db_import_json(self, response, stream_name, feed_info):
        pass

    @abstractmethod
    def json_result_to_csv(self, json_response):
        pass

    def get_date_time(self, datetime_str):
        # "2017-10-11T11:26:05Z" (Triangulum/Pi recorded data style)
        # "2017-10-11T11:34:09.2461304Z" (Triangulum/Pi interpolated data style)
        # "Thu, 12 Oct 2017 14:30:05 GMT"(BT Datahub style)
        # "2018-02-23T08:24:38.127Z" CDP date in accident entity.created field
        # "2017-10-01" CDP date in crime entity.occurred field

        ######### Truncation ###########
        # remove trailing Z
        datetime_str = str(datetime_str).rstrip('Z')
        # if it is a triangulum style date and there are too many digits in last (millisecs) field, then truncate
        if(re.match("^((\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{7,}))$", datetime_str)):
            datetime_str = datetime_str[0:26]


        ########## Matching ###########
        try:

            ### Triangulum like ###
            if (re.match("^((\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{6}))$", datetime_str)):
                # EG: "2017-10-11T11:26:05.246130" (Triangulum/Pi 'interpolated' data style - after truncation)
                result = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
            elif (re.match("^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})$", datetime_str)):
                # EG: "2017-10-11T11:26:05" (Triangulum/Pi 'recorded' data style - after truncation)
                result = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
            elif (re.match("^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})$", datetime_str)):
                result = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

            ### BT like ###
            elif(re.match("^(\w{3}), (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) GMT$", datetime_str)):
                # EG: "Thu, 12 Oct 2017 14:30:05 GMT" (BT Data hub style)
                result = datetime.datetime.strptime(datetime_str, '%a, %d %b %Y %H:%M:%S %Z')
            elif (re.match("^(\w{3}) (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) GMT$", datetime_str)):
                # EG: "Thu 12 Oct 2017 14:30:05 GMT"
                result = datetime.datetime.strptime(datetime_str, '%a %d %b %Y %H:%M:%S %Z')
            elif (re.match("^(\w{3}), (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})$", datetime_str)):
                # EG: "Thu, 12 Oct 2017 14:30:05"
                result = datetime.datetime.strptime(datetime_str, '%a, %d %b %Y %H:%M:%S')
            elif (re.match("^(\w{3}) (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})$", datetime_str)):
                # EG: "Thu 12 Oct 2017 14:30:05"
                result = datetime.datetime.strptime(datetime_str, '%a %d %b %Y %H:%M:%S')

            ### CDP like ###
            elif (re.match("^((\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{3}))$", datetime_str)):
                # EG: "2018-02-23T08:24:38.127Z" (CDP date in accident entity.created field)
                result = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
            elif (re.match("^((\d{4})-(\d{2})-(\d{2}))$", datetime_str)):
                # EG: "2017-10-01" CDP date in crime entity.occurred field
                result = datetime.datetime.strptime(datetime_str, '%Y-%m-%d')

            else:
                result = parse(datetime_str)
        except:
            raise ValueError('Unable to format datetime from given string: ' + datetime_str)

        return result

    def is_int(self, s):
        try:
            int(s)
            return True
        except:
            return False

    def is_float(self, s):
        try:
            float(s)
            return True
        except:
            return False

    def is_dict(self, s):
        try:
            dict(s)
            return True
        except:
            return False
