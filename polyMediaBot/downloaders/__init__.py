from polyMediaBot.downloaders.youtubeDownloader import YoutubeDownloader
from polyMediaBot.downloaders.vimeoDownloader import VimeoDownloader
from polyMediaBot.downloaders.instagramDownloader import InstagramDownloader

from polyMediaBot.core.videoDownloader import VideoDownloader
from polyMediaBot.constants import Downloader

from dataclasses import dataclass
from typing import Dict

downloaders: Dict[Downloader, VideoDownloader] = {
    "youtube": YoutubeDownloader,
    "vimeo": VimeoDownloader,
    "instagram": InstagramDownloader
}

class DownloaderFactory:
    @staticmethod
    def get(downloader: Downloader, *args, **kwargs) -> VideoDownloader:
        return downloaders[downloader](*args, **kwargs)
