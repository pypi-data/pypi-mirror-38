import os
from data_hub_call.selectedStreamsFiles import SelectedStreamsFiles
from data_hub_call.selectedStreamsDirectory import SelectedStreamsDirectory


class SelectedStreamsFromDBHubs(SelectedStreamsFiles):
    def __init__(self, data_sources_path, hubs):
        super(SelectedStreamsFromDBHubs, self).__init__(data_sources_path)
        self.initialise_directories(hubs)

    def initialise_directories(self, hubs):
        self.clear_all_streams()
        for hub in hubs:
            if hub.short_title not in self.stream_directories:
                self.stream_directories[hub.short_title] = SelectedStreamsDirectory(self.data_source_dir,
                                                                                   hub.short_title)

    def update_credentials(self, credentials):
        # self.clear_all_streams()
        for key in credentials:
            self.stream_directories[key].write_credential(credentials[key])


    def get_previously_selected_streams(self, user, streams):
        result = []
        for dir_key in self.stream_directories:
            result.extend(self.stream_directories[dir_key].get_previously_selected_streams(user, streams)['streams'])
        return result

    def add_to_streams(self, stream_params):
        self.stream_directories[stream_params['feed_info']['hub_short_title']].add_to_streams(stream_params)

    def remove_from_streams(self, stream_params):
        self.stream_directories[stream_params['feed_info']['hub_short_title']].remove_from_streams(stream_params)
