import unittest
from ybc_poetry import *


class MyTestCase(unittest.TestCase):
    def test_shici(self):
        content = '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不尽，轻舟已过万重山。'
        self.assertEqual(content, shici('早发白帝城', '李白'))


if __name__ == '__main__':
    unittest.main()
