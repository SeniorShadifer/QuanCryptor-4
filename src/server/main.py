import os

from termcolor import colored

import server.var
import server.const
import server.crypto
import server.route
from common import os_utils
from common import crypto_utils


def main():
    server.var.configuration = os_utils.load_configuration(
        f"{server.path.absolute_application_path}/configuration.json",
        default=server.var.default_configuration,
    )

    server.crypto.load_key()

    cert: str
    if not os.path.exists(server.var.configuration["cert_path"]) or not os.path.exists(
        server.var.configuration["key_path"]
    ):
        cert = server.crypto.load_cert().decode()
    else:
        with open(server.var.configuration["cert_path"], "r") as fin:
            cert = fin.read()
    server.var.cert = cert
    print(
        colored(
            f"Certificate hash: {crypto_utils.hash(cert.encode()).hex()}", color="cyan"
        )
    )

    server.route.flaskapp.run(
        host=server.var.configuration["ip"],
        port=server.var.configuration["port"],
        debug=server.var.configuration["debug"],
        use_reloader=server.var.configuration["use_reloader"],
        ssl_context=(
            server.var.configuration["cert_path"],
            server.var.configuration["key_path"],
        ),
    )
