from dataclasses import dataclass

@dataclass
class VideoInfo:
    link: str = None
    name: str = None
    views: int = None
    likes: int = None
    dislikes: int = None
    comments: int = None

@dataclass
class VideoProperties:
    resolution: str = None
    file_extension: str = None
