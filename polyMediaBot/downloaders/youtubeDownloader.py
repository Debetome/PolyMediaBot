from pytube import YouTube
from polyMediaBot.core.videoDownloader import VideoDownloader

class YoutubeDownloader(VideoDownloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.youtube = None
        self.video = None

    def _set_info(self):
        self.info.name = self.youtube.title
        self.info.views = self.youtube.views
        self.info.likes = None
        self.info.dislikes = None
        self.info.comments = None

    def _prepare_download(self):
        self.youtube = YouTube(self.info.url)
        self._set_info()
        self.video = self.youtube.streams.filter(
            file_extension=self.properties.file_extension,
            progressive=True,
            res=self.properties.resolution
        ).first()

    def download(self):
        self._prepare_download()

        try:
            self.video.download()
        except Exception as ex:
            raise Exception(ex)

    def cancel(self):
        pass
