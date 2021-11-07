from polyMediaBot.models import VideoInfo
from polyMediaBot.models import VideoProperties

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

@dataclass
class VideoParser(metaclass=ABCMeta):
    _info: VideoInfo = VideoInfo()
    _properties: VideoProperties = VideoProperties()

    def set_info(self, info: VideoInfo):
        self._info = info

    def set_properties(self, properties: VideoProperties):
        self._properties = properties

    @abstractmethod
    def parse(self):
        pass

    @property
    def info(self) -> VideoInfo:
        return self._info

    @property
    def properties(self) -> VideoProperties:
        return self._properties

