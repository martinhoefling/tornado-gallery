import unittest

from nose.tools import assert_equal
from PIL import Image

from tgallery.helper.picture import Picture


class TestPicture(unittest.TestCase):
    def test_resize_aspect_ratio(self):
        picture = Picture('some/picture')
        picture.image = Image.new("RGB", (150, 100), "white")
        picture.resize(75, 75)
        assert_equal((75, 50), picture.image.size)
