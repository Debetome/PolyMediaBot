from pytube import YouTube
from polyMediaBot.core.videoParser import VideoParser

class YoutubeParser(VideoParser):
    _youtube: YouTube = None
    _file: VideoParser = None

    def _set_info(self):
        self.info.url = self._file.url
        self.info.name = self._youtube.title
        self.info.views = self._youtube.views
        self.info.likes = None
        self.info.dislikes = None
        self.info.comments = None

    def parse(self):
        self._youtube = YouTube(self.info.url)

        if self.properties.file_type == "audio":
            self._file = self._youtube.streams.filter(
                only_audio=True
            ).first()
            return
        
        self._file = self._youtube.streams.filter(
            progressive=True,
            res=self.properties.resolution
        ).first()
        self._set_info()

    @property
    def youtube(self):
        return self._youtube

    @property
    def file(self):
        return self._file
