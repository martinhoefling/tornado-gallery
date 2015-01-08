import unittest
import io
from libxmp import XMPFiles
from libxmp import consts as xmpconsts

from nose.tools import assert_equal
from PIL import Image

from tgallery.util.picture import Picture


def generate_image(name, metadata=True, with_rating=True):
    testimage = Image.new("RGB", (150, 100), "white")
    testimage.save(name, 'JPEG')
    if metadata:
        testmetafile = XMPFiles(file_path=name, open_forupdate=True)
        testmeta = testmetafile.get_xmp()
        if with_rating:
            testmeta.set_property(xmpconsts.XMP_NS_XMP, 'xmp:Rating', '4')
        testmetafile.put_xmp(testmeta)
        testmetafile.close_file()

generate_image('test.jpg')
generate_image('no_rating.jpg', with_rating=False)
generate_image('no_meta.jpg', metadata=False)


class TestPicture(unittest.TestCase):
    def setUp(self):
        self.picture = Picture('test.jpg')

    def test_resize_aspect_ratio_x(self):
        self.picture.resize(75, 75)
        assert_equal((75, 50), self.picture._image.size)

    def test_resize_aspect_ratio_y(self):
        self.picture.resize(750, 75)
        assert_equal((112, 75), self.picture._image.size)

    def test_resize_zero_size(self):
        self.picture.resize(0, 0)
        assert_equal((1, 1), self.picture._image.size)

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
        self.picture.set_metadata({'rating': 2})
        assert_equal({'rating': 2}, self.picture.get_metadata())
        generate_image('test.jpg')

    def test_loading_default_if_nonexistent(self):
        self.picture = Picture('nonexistent')
        self.picture._read_image()
        assert_equal((800, 800), self.picture._image.size)

    def test_get_meta_no_meta_in_image(self):
        self.picture = Picture('no_meta.jpg')
        assert_equal({'rating': 0}, self.picture.get_metadata())

    def test_get_meta_no_rating_in_image(self):
        self.picture = Picture('no_rating.jpg')
        assert_equal({'rating': 0}, self.picture.get_metadata())

