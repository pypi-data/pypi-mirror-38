from data_hub_call.dataHubCall import DataHubCall
import requests
import json

class DataHubCallBTHub(DataHubCall):

    CORE_URL = "http://api.bt-hypercat.com"
    HUB_ID = 'BT-Hub'

    def __init__(self, request_info):
        """Return a BT data hub connection object which will
            be used to connect to [stream] using [credentials]
         """
        super(DataHubCallBTHub, self).__init__(self.CORE_URL, request_info, self.HUB_ID)

    class Factory:
        def create(self, request): return DataHubCallBTHub(request)

    def get_influx_db_import_json(self, response, stream_name, feed_info):
        """
        :param hypercat_response: [
              {
                "time": "Tue, 30 May 2017 15:30:04 GMT",
                "value": "556"
              },
              {
                "time": "Tue, 30 May 2017 15:15:05 GMT",
                "value": "526"
              },
              {
                "time": "Tue, 30 May 2017 15:00:04 GMT",
                "value": "507"
              },
              ...
        ]
        :param stream_name:
            eg: 'Manchester_carpark_spinningfields'
        """

        json_body_hypercat = json.loads(response)

        # Reformat JSON to be input into influx db.
        for item in json_body_hypercat:
            item['measurement'] = stream_name
            item['fields'] = {}
            if self.is_int(item['value']):
                item['fields']['value'] = int(item['value'])
            elif self.is_float(item['value']):
                item['fields']['value'] = float(item['value'])
            else:
                item['fields']['value'] = item['value']

            if'tagNames' in feed_info and len(feed_info['tagNames']) > 0:
                item['fields']['tagNames'] = feed_info['tagNames']
            item["tags"] = {}
            if('unitText' in feed_info and len(feed_info['unitText'].strip()) > 0):
                item["tags"]["unitText"] = feed_info['unitText'].strip()
            if 'longitude' in feed_info and feed_info['longitude'] != None:
                item["tags"]["longitude"] = feed_info['longitude']
            if 'latitude' in feed_info and feed_info['latitude'] != None:
                item["tags"]["latitude"] = feed_info['latitude']
            if 'href' in feed_info and feed_info['href'] != None:
                item["tags"]["href"] = feed_info['href']
            if ('type' in feed_info and feed_info['type'] != None):
                item["tags"]["type"] = feed_info['type']
            del item['value']

        return json_body_hypercat


    def json_result_to_csv(self, json_result):
        result = ''
        for datetime_value in json.loads(json_result):
            result += datetime_value['time'] + ',' + datetime_value['value'] + '\n'
        return result



    def call_api_fetch(self, params, output_format='application/json', get_latest_only=True):
        result = {}

        url_string = self.request_info.url_string()


        # passing the username and required output format
        headers_list = {"x-api-key": self.request_info.username, "Accept": output_format}
        #return "Username: " +cred.username + "; Api-key: " + cred.api_key + "; url: " + url_string

        if(get_latest_only and self.request_info.last_fetch_time != None):
            #Start date needs to be in format: 2015-05-07T12:52:00Z
            params['start'] = self.request_info.last_fetch_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            if 'start' in params:
                del params['start']

        try:
            hub_result = requests.get(url_string,
                                timeout=10.000,
                                auth=(self.request_info.api_key, ':'),
                                params=params,
                                headers=headers_list)
        except:
            raise ConnectionError("Error connecting to BT-hub - check internet connection.")
        if hub_result.ok == False:
                raise ConnectionRefusedError("Connection to BT-Hub refused: " + hub_result.reason)


        result_content = hub_result.content.decode("utf-8")

        json_result_content = json.loads(result_content)
        newlist = []

        if(get_latest_only):
            if(len(json_result_content) > 0):
                try:
                    newlist = sorted(json_result_content,
                                     key=lambda k: self.get_date_time(k["time"]),
                                     reverse=True)
                    most_recent = newlist[0]["time"]
                    self.request_info.last_fetch_time = self.get_date_time(most_recent)
                except ValueError as e:
                    result['ok'] = False
                    result['reason'] = str(e)
                except Exception as e:
                    result['ok'] = False
                    result['reason'] = 'Problem sorting results by date to get latest only. ' + str(e)

        result['content'] = json.dumps(json_result_content)

        result['available_matches'] = len(json_result_content)
        result['returned_matches'] = len(newlist)
        return result


    def call_api_post(self, eeml):
        # registered user name
        #username = "AnnGledson"
        # API key given to the user
        #api_key = '8a0b0d8c-bf4e-44d5-b34d-a2d5f139918a'  # AnnGledson2
        # choose output format - can be json or xml
        output_format = 'application/json'
        url_string = self.request_info.url_string()

        # 'http://api.bt-hypercat.com/'+ stream.feedType+'/feeds/'+stream.feed_id+'/datastreams/'+\
        #             stream.datastream_id+'/datapoints'

        # -----------------------------------#
        # Request URL Parameters

        # start_dt = datetime.strptime( "2017-01-01 00:00:00", "%Y-%m-%d %H:%M:%S" )
        # payload = {'start': start_dt}

        #for cred in self.credentials:
        # passing the username and required output format
        headers_list = {"x-api-key": self.request_info.username, "Accept":"*/*", "Content-Type":"text/xml"}
        #-H 'Content-Type:text/xml' -H 'Accept:*/*'
        #-X POST -d@{filename}

        return requests.post(url_string,
                               eeml,
                                auth=(self.request_info.api_key, ':'),
                                headers=headers_list)
