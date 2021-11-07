import unittest
from polyMediaBot.parsers import YoutubeParser
from polyMediaBot.models import VideoInfo
from polyMediaBot.models import VideoProperties

class TestYoutubeParserCase(unittest.TestCase):
    def test_fetch_best_quality(self):
        parser = YoutubeParser()
        properties = VideoProperties()
        info = VideoInfo()

        info.url = str(open("polyMediaBot/tests/url.txt").read().strip())

        properties.resolution = "720p"
        properties.file_type = "video"
        properties.duration = None

        parser.set_info(info)
        parser.set_properties(properties)

        parser.parse()


    def test_fetch_medium_quality(self):
        parser = YoutubeParser()
        properties = VideoProperties()
        info = VideoInfo()

        info.url = str(open("polyMediaBot/tests/url.txt").read().strip())

        properties.resolution = "360p"
        properties.file_type = "video"
        properties.duration = None

        parser.set_info(info)
        parser.set_properties(properties)

        parser.parse()

    def test_fetch_lowest_quality(self):
        parser = YoutubeParser()
        properties = VideoProperties()
        info = VideoInfo()

        info.url = str(open("polyMediaBot/tests/url.txt").read().strip())

        properties.resolution = "144p"
        properties.file_type = "video"
        properties.duration = None

        parser.set_info(info)
        parser.set_properties(properties)

        parser.parse()

    def test_fetch_audio(self):
        parser = YoutubeParser()
        properties = VideoProperties()
        info = VideoInfo()

        info.url = str(open("polyMediaBot/tests/url.txt").read().strip())

        properties.resolution = None
        properties.file_type = "audio"
        properties.duration = None

        parser.set_info(info)
        parser.set_properties(properties)

        parser.parse()

