from polyMediaBot.core.videoDownloader import VideoDownloader

class InstagramDownloader(VideoDownloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def download(self):
        pass

    def cancel(self):
        pass
