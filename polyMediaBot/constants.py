from enum import Enum, auto

class State(Enum):
    SELECT_PARSER = 0
    PARSING_URL = 1
    SELECT_TYPE = 2
    SELECT_QUALITY = 3

class Downloader(Enum):
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    INSTAGRAM = "instagram"

class Type(Enum):
    VIDEO = "mp4"
    AUDIO = "mp3"
    GIF = "gif"

class Quality(Enum):
    HIGH = "720p"
    MEDIUM = "360p"
    LOW = "144p"
