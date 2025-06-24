from termcolor import colored

import server.const
import server.route
import server.var
from common import os_utils


def main():
    server.var.configuration = os_utils.load_configuration(
        f"{server.path.absolute_application_path}/configuration.json",
        default={"ip": "0.0.0.0", "port": 8254, "debug": False},
    )

    server.route.server.run(
        host=server.var.configuration["ip"],
        port=server.var.configuration["port"],
        debug=server.var.configuration["debug"],
    )
