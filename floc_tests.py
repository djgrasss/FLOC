#!/usr/bin/env python

from floc import FLOC
import unittest


class TestFLOC(unittest.TestCase):

    def setUp(self):
        self.base_url = ("https://www.facebook.com/dialog/oauth?" +
                         "response_type=code" +
                         "&scope=email%2Cuser_likes" +
                         "&client_id=123456789" +
                         "&redirect_uri=http%3A%2F%2Fwww.example.com%2Fauth%2Ffacebook%2Fcallback")
        self.raw_url_vulnerable = self.base_url
        self.raw_url_not_vulnerable = (self.base_url +
                                       "&state=ac597a005kikasdecc8f16c4c61e368285271dad63653505")

    def test_parse_raw_url_vulnerable(self):
        floc_object = FLOC()
        self.assertTrue(floc_object.check_vulnerable(self.raw_url_vulnerable))

    def test_parse_raw_url_not_vulnerable(self):
        floc_object = FLOC()
        self.assertTrue(floc_object.check_vulnerable(self.raw_url_not_vulnerable))

if __name__ == '__main__':
    unittest.main()
