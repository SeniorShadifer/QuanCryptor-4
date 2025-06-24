import unittest

import common.crypto_utils


class TestHashPasswordFunction(unittest.TestCase):
    def test(self):
        self.assertEqual(
            "1f0ae7cbb5de9e36bae2cbcb36e7412160d1c2f20994d893f8b9d1e59df377b0",
            common.crypto_utils.hash_password(
                b"Hello, world!", b"test_salt", iterations=10
            ).hex(),
        )
