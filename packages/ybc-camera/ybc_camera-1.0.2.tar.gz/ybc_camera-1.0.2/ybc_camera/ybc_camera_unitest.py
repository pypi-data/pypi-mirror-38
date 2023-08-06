import unittest
from ybc_camera import *


class MyTestCase(unittest.TestCase):
    def test_camera(self):
        self.assertIsNotNone(camera())


if __name__ == '__main__':
    unittest.main()
