from polyMediaBot.parsers.youtubeParser import YoutubeParser
from polyMediaBot.parsers.vimeoParser import VimeoParser
from polyMediaBot.parsers.instagramParser import InstagramParser

from polyMediaBot.core.videoParser import VideoParser

from dataclasses import dataclass
from typing import Dict

ParserFactory: Dict[str, VideoParser] = {
    "youtube": YoutubeParser,
    "vimeo": VimeoParser,
    "instagram": InstagramParser
}
