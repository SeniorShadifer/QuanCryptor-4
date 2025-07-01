import unittest

import common.crypto_utils


class TestHashWithSaltFunction(unittest.TestCase):
    def test_when_password_is_bytes(self):
        self.assertEqual(
            "1f0ae7cbb5de9e36bae2cbcb36e7412160d1c2f20994d893f8b9d1e59df377b0",
            common.crypto_utils.hash_with_salt(
                b"Hello, world!", b"test_salt", iterations=10
            ).hex(),
        )

    def test_when_password_is_str(self):
        self.assertEqual(
            "1f0ae7cbb5de9e36bae2cbcb36e7412160d1c2f20994d893f8b9d1e59df377b0",
            common.crypto_utils.hash_with_salt(
                "Hello, world!", b"test_salt", iterations=10
            ).hex(),
        )
