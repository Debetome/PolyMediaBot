import unittest
import os

from polyMediaBot.parsers import ParserFactory
from polyMediaBot.models import VideoInfo
from polyMediaBot.models import VideoProperties
from polyMediaBot.utils import download

class TestUtilsCase(unittest.TestCase):
    def test_download_file(self):
        parser = ParserFactory.get("youtube")
        properties = VideoProperties()
        info = VideoInfo()

        info.url = str(open("polyMediaBot/tests/url.txt").read().strip())

        properties.resolution = "720p"
        properties.file_type = "video"

        parser.set_properties(None, properties)
        parser.set_info(info)
        parser.parse()

        filename = download.download_file(parser.info.url)
        self.assertIsInstance(filename, str)
        self.assertEqual(filename, "file.mp4")
        os.system(f"rm -rf {filename}")

