import os
import json
from data_hub_call.requestInfoFetchList import RequestInfoFetchList

class SelectedStreamsDirectory(object):
    """A directory for storing selected stream and credentials info"""


    def __init__(self, home_dir, hub_title, credential=None):
        self.hub_title = hub_title
        self.directory = os.path.join(home_dir, self.hub_title)
        self.file_spec = os.path.join(self.directory, self.hub_title + '_request_list.json')
        self.credentials_spec = os.path.join(self.directory, self.hub_title + '_credentials.json')
        self.credential = credential
        self.api_streams = RequestInfoFetchList()

        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)

        if credential is not None:
            self.write_credential()
        else:
            self.read_credential()

        self.get_streams_from_file()


    def get_selected_stream_ids(self):
        return self.api_streams.get_list_of_users_stream_ids()


    def write_credential(self, credential):
        self.credential = credential
        if not os.path.exists(os.path.dirname(self.credentials_spec)):
            os.makedirs(os.path.dirname(self.credentials_spec), exist_ok=True)
        try:
            with open(self.credentials_spec, "w") as f_creds:
                json.dump(self.credential, f_creds)
        except Exception as err:
            raise IOError('Unable to open or write to credentials file: ' + self.credentials_spec + '. ' + str(err))


    def read_credential(self):
        creds_json = {}
        try:
            with open(self.credentials_spec, "r+") as f_creds:
                creds_json = json.load(f_creds)
        except Exception as err:
            print('Unable to read credentials file: ' + self.credentials_spec + '. ' + str(err))
        self.credential = creds_json



    def get_streams_from_file(self):
        # Read from selected streams files
        self.api_streams.clear_all()
        api_streams_json = []

        # Get the streams
        try:
            with open(self.file_spec) as f_requests:
                api_streams_json = json.load(f_requests)
                f_requests.close()
        except Exception as err:
            print('Unable to read ' + self.hub_title + ' streams file ' + self.file_spec + ': ' + str(err))

        if 'api_key' in self.credential:
            api_key = self.credential['api_key']
        else:
            api_key = None

        if 'username' in self.credential:
            username = self.credential['username']
        else:
            username = None

        for stream_params in api_streams_json:
            try:
                self.api_streams.append_request(
                    self.hub_title, stream_params, api_key=api_key, username=username)
            except Exception as err:
                print('Unable to create ' + self.hub_title + ' stream from : ' + json.dumps(stream_params)
                      + ': ' + str(err))


    def clear_all_streams(self):
        self.api_streams.clear_all()
        new_file = []

        if os.path.exists(os.path.dirname(self.directory)):
            with open(self.file_spec, "w+") as f_out:
                json.dump(new_file, f_requests)

    def add_to_streams(self, stream_params):
        stream_href = stream_params['feed_info']['href']

        if not os.path.exists(os.path.dirname(self.file_spec)):
            os.makedirs(os.path.dirname(self.file_spec), exist_ok=True)

        try:
            with open(self.file_spec)  as f_requests:
                try:
                    api_streams_json = json.load(f_requests)
                except Exception as err:
                    api_streams_json = []
                for api_stream in api_streams_json:
                    if api_stream['feed_info']['href'] == stream_href:
                        break
                else:
                    api_streams_json.append(stream_params)
            with open(self.file_spec, "w+") as f_requests:
                json.dump(api_streams_json, f_requests)

        except Exception as err:
            raise IOError('Unable to open streams file: ' + self.file_spec + ': ' + str(err))

        self.get_streams_from_file()


    def remove_from_streams(self, stream_params):
        stream_href = stream_params['feed_info']['href']

        if not os.path.exists(os.path.dirname(self.file_spec)):
            os.makedirs(os.path.dirname(self.file_spec), exist_ok=True)

        try:
            with open(self.file_spec) as f_requests:
                try:
                    api_streams_json = json.load(f_requests)
                except:
                    api_streams_json = []
                for api_stream in api_streams_json:
                    if api_stream['feed_info']['href'] == stream_href:
                        api_streams_json.remove(api_stream)
            with open(self.file_spec, "w+") as f_requests:
                json.dump(api_streams_json, f_requests)

        except Exception as err:
            raise IOError('Unable to open streams file: ' + self.file_spec + ': ' + str(err))

        self.get_streams_from_file()

    def get_previously_selected_streams(self, user, streams):
        previous_streams_list = {'streams': []}

        for stream in streams:
            stream_dict = {}
            stream_dict["datetime"] = str(stream.added_date)
            str_params = stream.parameters.replace("'", '"')
            stream_dict["parameters"] = json.loads(str_params)
            stream_dict["users_name"] = user.username
            previous_streams_list['streams'].append(stream_dict)

        return previous_streams_list