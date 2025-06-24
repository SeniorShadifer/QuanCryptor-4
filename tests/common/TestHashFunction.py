import unittest

import common.crypto_utils


class TestHashFunction(unittest.TestCase):
    def test(self):
        self.assertEqual(
            "315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3",
            common.crypto_utils.hash(b"Hello, world!").hex(),
        )
