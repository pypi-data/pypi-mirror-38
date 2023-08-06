from data_hub_call.dataHubCall import DataHubCall
import requests
import json

TIMESERIES_TIME_FIELD = ["latest","to"]
TIMESERIES_VALUE_FIELD = ["latest","value"]


class DataHubCallCityVervePoP(DataHubCall):

    CORE_URL = "https://api.cityverve.org.uk/v1"
    HUB_ID = 'CityVervePoP'

    def __init__(self, request_info): #, username, api_key):
        """Return a CDP connection object which will
            be used to connect to [stream] using [credentials]
         """
        super(DataHubCallCityVervePoP, self).__init__(self.CORE_URL, request_info, self.HUB_ID)

    class Factory:
        def create(self, request): return DataHubCallCityVervePoP(request)

    def get_influx_db_import_json(self, response, stream_name, feed_info):
        """
        :param response: [
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
            if(self.is_int(item['value'])):
                item['fields']['value'] = int(item['value'])
            elif(self.is_float(item['value'])):
                item['fields']['value'] = float(item['value'])
            else:
                item['fields']['value'] = item['value']

            if('tagNames' in feed_info and len(feed_info['tagNames']) > 0):
                item['fields']['tagNames'] = feed_info['tagNames']
            item["tags"] = {}
            if('unitText' in feed_info and len(feed_info['unitText'].strip()) > 0):
                item["tags"]["unitText"] = feed_info['unitText'].strip()
            if('longitude' in feed_info and feed_info['longitude'] != None):
                item["tags"]["longitude"] = feed_info['longitude']
            if ('latitude' in feed_info and feed_info['latitude'] != None):
                item["tags"]["latitude"] = feed_info['latitude']
            if ('href' in feed_info and feed_info['href'] != None):
                item["tags"]["href"] = feed_info['href']
            if ('type' in feed_info and feed_info['type'] != None):
                item["tags"]["type"] = feed_info['type']
            del item['value']

        return json_body_hypercat


    def call_api_fetch(self, params, output_format='application/json', get_latest_only=True,
                       time_field=TIMESERIES_TIME_FIELD, value_field=TIMESERIES_VALUE_FIELD):
        result = {}

        # Make request to CDP hub
        url_string = self.request_info.url_string()

        try:
            hub_result = self.get_request(url_string, params, output_format, get_latest_only)
        except Exception as err:
            raise ConnectionError("Error connecting to CDP-hub - check internet connection. " + str(err))
        if hub_result.ok == False:
            raise ConnectionRefusedError("Connection to CDP-Hub refused: " + hub_result.reason)

        result_content = hub_result.content.decode("utf-8")
        json_result_content= json.loads(result_content)

        json_result_timeseries = []
        for item in json_result_content:
            for data_point in item['timeseries']:
                try:
                    json_result_timeseries.append(
                        {
                            'time': self.get_time(data_point, time_field),
                            'value': self.get_val_from_path(data_point, value_field)
                         }
                    )
                except:
                    break

        available_match_count = len(json_result_timeseries)
        if available_match_count == 0:
            result['ok'] = False
            result['available_matches'] = 0
            result['returned_matches'] = 0
            result['reason'] = 'No times/values with correct formats found.'
            return result

        # No Date params allowed in call to hub, so apply get latest only to hub results here...
        if (get_latest_only and self.request_info.last_fetch_time != None):
            try:
                # Filter python objects with list comprehensions
                new_content = [x for x in json_result_timeseries
                               ###### Due to CDP having to fetch children [2] ######
                               # For CDP we also include results with time == last_fetch_time (>=), as we have to keep
                               # aggregating all results with same time, so latest time value might still be incrementing
                               if self.get_date_time(x['time']) >= self.request_info.last_fetch_time]

                json_result_timeseries = new_content
                result['content'] = json.dumps(json_result_timeseries)
            except ValueError as e:
                result['ok'] = False
                result['reason'] = str(e)
            except Exception as e:
                result['ok'] = False
                result['reason'] = 'Problem sorting results by date to get latest only. ' + str(e)

        result['available_matches'] = available_match_count
        result['returned_matches'] = len(json_result_timeseries)

        # Set last_fetch_time for next call
        if get_latest_only:
            if len(json_result_timeseries) > 0:
                try:
                    newlist = sorted(json_result_timeseries,
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

        # Return result
        result['content'] = json.dumps(json_result_timeseries)
        result['ok'] = True
        return result

    def get_request(self, url, params, output_format, get_latest_only):
        # passing the username and required output format
        headers_list = {    "Authorization": self.request_info.api_key,
                            "Accept": output_format}

        if get_latest_only and self.request_info.last_fetch_time != None:
            # Start date needs to be in format: 2015-05-07T12:52:00Z
            params['start'] = self.request_info.last_fetch_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            if 'start' in params:
                del params['start']

        try:
            hub_result = requests.get(url,
                                timeout=10.000,
                                params=params,
                                headers=headers_list)
            if hub_result.ok == False:
                raise ConnectionRefusedError("Connection to CDP refused: " + hub_result.reason)
        except:
            raise ConnectionError("Error connecting to CDP hub - check internet connection.")

        return hub_result

    def get_time(self, json_dict, list_path):
        #2018-02-23T08:24:38.127Z or 2017-10-01
        time = self.get_val_from_path(json_dict, list_path)
        try:
            date_time = self.get_date_time(time)
        except:
            raise ValueError("Time value is invalid")

        if date_time.time():
            # Contains time, so group_by = hour
            time = str(date_time.date()) + 'T' + str(date_time.hour) + ':00:00.000Z'
        #Otherwise leave as it and group_by will be daily (or monthly or yearly depending on granularity)

        return time


    def get_val_from_path(self, json_dict, list_path):
        result = json_dict
        for val_field in list_path:
            result = result[val_field]
        return result




    def call_api_fetch_accidents(self, params, output_format='application/json', get_latest_only=True,
                       get_children_as_time_series=True, time_field="entity.occurred", value_field="value"):
        result = {}

        # Make request to CDP hub
        url_string = self.request_info.url_string()
        temp_get_latest = False if (get_children_as_time_series == True) else get_latest_only;
        hub_result = self.get_request(url_string, params, output_format, temp_get_latest)


        result_content = hub_result.content.decode("utf-8")

        json_result_content = json.loads(result_content)

        ###### Due to CDP having to fetch children [1] ######
        # Get entity children
        if get_children_as_time_series:
            json_result_children = []
            for entity in json_result_content:
                if 'uri' in entity:
                    child_uri = entity['uri']
                elif 'url' in entity:
                    child_uri = entity['url']
                elif 'href' in entity:
                    child_uri = entity['href']
                child_result = self.get_child_for_time_series(child_uri, params, output_format, get_latest_only)
                if child_result is not None:
                    json_result_children.append(child_result)
            json_result_content = self.get_children_as_time_series(
                json_result_children, time_field=time_field, value_field=value_field)

        available_matches = len(json_result_content)

        # No Date params allowed in call to hub, so apply get latest only to hub results here...
        if (get_latest_only and self.request_info.last_fetch_time != None):
            try:
                # Filter python objects with list comprehensions
                new_content = [x for x in json_result_content
                               ###### Due to CDP having to fetch children [2] ######
                               # For CDP we also include results with time == last_fetch_time (>=), as we have to keep
                               # aggregating all results with same time, so latest time value might still be incrementing
                               if self.get_date_time(x['time']) >= self.request_info.last_fetch_time]

                json_result_content = new_content
                result['content'] = json.dumps(json_result_content)
            except ValueError as e:
                result['ok'] = False
                result['reason'] = str(e)
            except Exception as e:
                result['ok'] = False
                result['reason'] = 'Problem sorting results by date to get latest only. ' + str(e)

        result['available_matches'] = available_matches
        result['returned_matches'] = len(json_result_content)

        # Set last_fetch_time for next call
        newlist = []
        if get_latest_only:
            if len(json_result_content) > 0:
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

        # Return result
        result['content'] = json.dumps(json_result_content)
        return result

    def get_children_as_time_series(self, json_children, time_field=['entity','occurred']):
        result = []
        time_field_as_path_list = time_field.strip().split(".")
        if len(time_field_as_path_list) == 0:
            return result

        """
        FROM:
        {
            "id": "60411677",
            "uri": "https://api.cityverve.org.uk/v1/entity/crime/60411677",
            "type": "crime",
            "name": "Anti Social Behaviour - On or near Manor Road",
            "loc": {},
            "entity": {
                "category": "Anti Social Behaviour",
                "occurred": "2017-10-01",
                "area": "On or near Manor Road",
                "outcome": {
                    "status": null,
                    "resolved": null
                }
            },
            "instance": {...},
            "legal": [..]
        }, {}, {}, ...

        TO:
        {
            "time": "2017-10-01",
            "value": "556"
        },
        {...}, {...}, ..."""

        # get times
        result_dict = {}
        for child in json_children:
            time = self.get_time(child[0], time_field_as_path_list)
            if time in result_dict:
                result_dict[time] += 1
            else:
                result_dict[time] = 1

        # turn lookup dict (result_dict) into final list
        for key, value in result_dict.items():
            temp = {'time': key, 'value': value}
            result.append(temp)

        return result

    def get_child_for_time_series(self, uri, params, output_format='application/json', get_latest_only=True):
        # Make request to CDP hub
        hub_result = self.get_request(uri, params, output_format, get_latest_only)
        return json.loads(hub_result.content.decode("utf-8"))

    def json_result_to_csv(self, json_result):
        result = ''
        for datetime_value in json.loads(json_result):
            result += datetime_value['time'] + ',' + datetime_value['value'] + '\n'
        return result