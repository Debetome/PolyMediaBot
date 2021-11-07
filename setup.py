from setuptools import setup
from setuptools import Extension

extensions = {
    "downloader": Extension(
                    sources=["polyMediaBot/utils/downloader.c"]),
                    libraries=["curl"]),
    "uploader": None,
    "mesher": None
}

setup(
    name="Poly media bot",
    version="1.0"
    ext_modules=[
        extensions["downloader"]
    ]
)
