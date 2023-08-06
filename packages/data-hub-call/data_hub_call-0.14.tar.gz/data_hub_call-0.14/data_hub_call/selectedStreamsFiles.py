import os

class SelectedStreamsFiles(object):
    def __init__(self, data_sources_path):
        self.data_source_dir = data_sources_path
        self.stream_directories = {}


    def get_streams_from_file(self):
        for dir_key in self.stream_directories:
            self.stream_directories[dir_key].get_streams_from_file()


    def clear_all_streams(self):
        for dir_key in self.stream_directories:
            self.stream_directories[dir_key].clear_all_streams()


    def get_selected_stream_ids(self):
        result = []
        for dir_key in self.stream_directories:
            result.extend(self.stream_directories[dir_key].get_selected_stream_ids())
        return result



    def get_selected_stream_ids(self):
        result = []
        for dir_key in self.stream_directories:
            result.extend(self.stream_directories[dir_key].get_selected_stream_ids())
        return result


    def get_api_streams(self):
        result = []
        for dir_key in self.stream_directories:
            result.extend(self.stream_directories[dir_key].api_streams.requests)
        return result

