import unittest

import client.utils


class TestAddressToKeyPathFunction(unittest.TestCase):
    def test(self):
        self.assertEqual(
            "server_certificates/example.com.8254.pem",
            client.utils.address_to_key_path("example.com:8254"),
        )
