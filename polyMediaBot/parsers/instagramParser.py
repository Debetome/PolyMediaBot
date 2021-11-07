import requests
from polyMediaBot.core.videoParser import VideoParser

class InstagramParser(VideoParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_info(self):
        self.info.url = None
        self.info.name = None
        self.info.likes = None

    def parse(self):
        pass
