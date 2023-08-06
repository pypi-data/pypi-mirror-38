import unittest
from .ybc_animal import *


path_pic = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'test.jpg')


class MyTestCase(unittest.TestCase):
    def test_what(self):
        self.assertEqual('狗', what(path_pic))

    def test_breed(self):
        self.assertEqual('金毛狗', breed(path_pic))

    def test_desc(self):
        self.assertIsNotNone(desc(path_pic))


if __name__ == '__main__':
    unittest.main()
