import os
from data_hub_call.selectedStreamsFiles import SelectedStreamsFiles
from data_hub_call.selectedStreamsDirectory import SelectedStreamsDirectory

class SelectedStreamsFromFileHubs(SelectedStreamsFiles):
    def __init__(self, data_sources_path):
        super(SelectedStreamsFromFileHubs, self).__init__(data_sources_path)
        self.initialise_directories()

    def initialise_directories(self):
        # list sub directories
        for root, dirs, files in os.walk(self.data_source_dir):
            # iterate through them
            for dir in dirs:
                if dir not in self.stream_directories:
                    self.stream_directories[dir] = SelectedStreamsDirectory(self.data_source_dir, dir)
        self.get_streams_from_file()






