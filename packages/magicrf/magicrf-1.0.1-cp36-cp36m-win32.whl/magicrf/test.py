# -*- coding:utf-8 -*-
""" Test library for m100 """
# !/usr/bin/python
# Python:   3.6.5
# Platform: Windows/Linux/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test library m100 Module.
# History:  2018-10-24 Wheel Ver:1.0.0 [Heyn] Initialize

import unittest

from magicrf import m100

class TestMagicRF(unittest.TestCase):
    """Test MagicRF variant.
    """

    def do_basics(self, module):
        """Test basic functionality.
        """
        # very basic example
        # self.assertEqual(module.maxim8(b'123456789'), 0xA1)
        pass

    def test_basics(self):
        """Test basic functionality.
        """
        # self.do_basics(m100)
        print('Query {}'.format(m100.query()))
        print('Get PA Power {}'.format(m100.power()))
        print('Set PA Power {}'.format(m100.power(22.0)))
        print('Mode {}'.format(m100.mode(m100.MODE_DENSE_READER)))


    def test_basics_c(self):
        """Test basic functionality of the extension module.
        """
        self.do_basics(m100)


if __name__ == '__main__':
    unittest.main()
