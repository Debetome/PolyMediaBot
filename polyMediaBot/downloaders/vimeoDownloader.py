from polyMediaBot.core.videoDownloader import VideoDownloader

class VimeoDownloader(VideoDownloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def download_video(self):
        pass

    def cancel_download(self):
        pass
