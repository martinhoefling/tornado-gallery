from PIL.ExifTags import TAGS
import pyexiv2

# import exiftool
#
# et = exiftool.ExifTool()

TAGS[0x4746] = 'Rating'
TAGS[0x4749] = 'RatingPercent'
TAGS[0xc4a5] = 'PrintImageMatching'
TAGS[0x000b] = 'ProcessingSoftware'


class Picture(object):
    def __init__(self, filename):
        self.filename = filename

    def get_metadata(self):
        metadata = pyexiv2.ImageMetadata(self.filename)
        metadata.read()
        meta_keys = metadata.exif_keys + metadata.iptc_keys + metadata.xmp_keys
        return {key: metadata[key].raw_value for key in meta_keys}

    # class Picture(object):
    #     def __init__(self, filename):
    #         self.image = Image.open(filename)
    #
    #     def get_metadata(self):
    #         ret = {}
    #         info = self.image._getexif()
    #         if info != None:
    #             for tag, value in info.items():
    #                 decoded = TAGS.get(tag, tag)
    #                 print '#########'
    #                 print tag
    #                 print decoded
    #                 print value
    #                 # try:
    #                 #     int(decoded)
    #                 # except ValueError:
    #                 if not decoded in ('MakerNote','PrintImageMatching'):
    #                     ret[decoded] = value
    #
    #         return ret




    # #!/usr/bin/python3
    #   2
    #   3 from gi.repository import GExiv2
    #   4
    #   5 exif = GExiv2.Metadata('IMG_1234.JPG')
    #   6
    #   7 # longitude, latitude, altitude
    #   8 exif.set_gps_info(-79.3969702721, 43.6295057244, 76)
    #   9
    #  10 # Using dict notation like this reads/writes RAW string values
    #  11 # into the EXIF data, with no modification/interpolation by GExiv2.
    #  12 # Refer to GExiv2.py to see what kind of convenience methods are
    #  13 # supplied for setting/getting non-string values.
    #  14 IPTC = 'Iptc.Application2.'
    #  15 exif[IPTC + 'City'] = 'Toronto'
    #  16 exif[IPTC + 'ProvinceState'] = 'Ontario'
    #  17 exif[IPTC + 'CountryName'] = 'Canada'
    #  18
    #  19 exif.save_file()
