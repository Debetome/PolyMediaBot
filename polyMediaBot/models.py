from dataclasses import dataclass

@dataclass
class VideoInfo:
    url: str = None
    name: str = None
    views: int = None
    likes: int = None
    dislikes: int = None
    comments: int = None

@dataclass
class VideoProperties:
    resolution: str = None
    file_type: str = None
    duration: float = None
