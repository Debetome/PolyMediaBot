from setuptools import setup
from setuptools import Extension

setup(
    name="upload-lib",
    version="0.1",
    ext_modules=[Extension("upload", sources=["uploader.c"], libraries=["curl"])]
)
