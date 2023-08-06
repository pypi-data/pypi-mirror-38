import unittest
from ybc_face import *


class MyTestCase(unittest.TestCase):
    def test_gender(self):
        self.assertEqual('男', gender('test.jpg'))

    def test_glass(self):
        self.assertEqual(False, glass('test.jpg'))

    def test_no_face(self):
        self.assertEqual('图片中找不到人哦~', info('cup.jpg'))

    def test_png(self):
        self.assertEqual('图片中找不到人哦~', info('rgba.png'))


if __name__ == '__main__':
    unittest.main()
