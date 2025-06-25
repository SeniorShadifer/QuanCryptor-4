import unittest
import pathlib
import json
import os

from common import os_utils


class TestLoadConfigurationFunction(unittest.TestCase):
    absolute_test_path = os.path.dirname(os.path.abspath(__file__))
    configuration_file_name = f"{absolute_test_path}/test_configuration.json"

    def test_when_file_exists(self):
        default = {"ip": "0.0.0.0", "port": 8254, "debug": False}
        user_configuration = {"ip": "localhost", "port": 443}

        expected_value = user_configuration
        expected_value["debug"] = default["debug"]

        with open(self.configuration_file_name, "w") as fout:
            fout.write(json.dumps(user_configuration))

        self.assertEqual(
            expected_value,
            os_utils.load_configuration(self.configuration_file_name, default),
        )

    def test_when_file_not_exists(self):
        if os.path.exists(self.configuration_file_name):
            pathlib.Path.unlink(self.configuration_file_name)

        default = {"key": "value"}
        self.assertEqual(
            default, os_utils.load_configuration(self.configuration_file_name, default)
        )

    def delete_configuration_file(self):
        if os.path.exists(self.configuration_file_name):
            pathlib.Path.unlink(self.configuration_file_name)
