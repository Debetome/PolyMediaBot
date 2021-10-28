from polyMediaBot.models import VideoInfo
from polyMediaBot.models import VideoProperties

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

@dataclass
class VideoDownloader(metaclass=ABCMeta):
    info: VideoInfo = VideoInfo()
    properties: VideoProperties = VideoProperties()
    completed: bool = False

    def set_info(self, info: VideoInfo):
        self.info = info

    def set_properties(self, properties: VideoProperties):
        self.properties = properties

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

