import unittest
import io
from libxmp import XMPFiles
from libxmp import consts as xmpconsts

from nose.tools import assert_equal
from PIL import Image

from tgallery.helper.picture import Picture


def generate_test_image():
    global testimage, testmetafile, testmeta
    testimage = Image.new("RGB", (150, 100), "white")
    testimage.save('test.jpg', 'JPEG')
    testmetafile = XMPFiles(file_path='test.jpg', open_forupdate=True)
    testmeta = testmetafile.get_xmp()
    testmeta.set_property(xmpconsts.XMP_NS_XMP, 'xmp:Rating', '4')
    testmetafile.put_xmp(testmeta)
    testmetafile.close_file()


generate_test_image()


class TestPicture(unittest.TestCase):
    def setUp(self):
        self.picture = Picture('test.jpg')

    def test_resize_aspect_ratio(self):
        self.picture.resize(75, 75)
        assert_equal((75, 50), self.picture.image.size)

    def test_get_metadata(self):
        assert_equal({'rating': 4}, self.picture.get_metadata())

    def test_get_content(self):
        content = self.picture.get_content()
        reference = Image.open('test.jpg')
        reference.load()
        buf = io.BytesIO()
        reference.save(buf, format="JPEG")
        refcontent = buf.getvalue()
        buf.close()
        assert_equal(refcontent, content)

    def test_write_metadata(self):
        self.picture.set_rating(2)
        assert_equal({'rating': 2}, self.picture.get_metadata())
        generate_test_image()
