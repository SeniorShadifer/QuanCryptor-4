import traceback
import base64
import json
import os

import requests
from termcolor import colored
from webview import JavascriptException

import client.utils, client.main, client.path, client.db
from common import crypto_utils


class Api:
    def print(self, text):
        print(text)

    def get_server_list(self):
        return client.db.cursor.execute("SELECT address FROM servers").fetchall()

    def add_server(self, address: str, certificate_hash: str, password: str = None):
        def output(text, color: str = "white"):
            try:
                print(colored(text, color=color))
                client.main.webview.active_window().evaluate_js(
                    f"""let output = document.getElementById('result_0');
                        output.innerHTML = '{text}';
                        output.style.setProperty('color', '{color}');
                        """
                )
            except JavascriptException as e:
                traceback.print_exc()

        try:
            output("Getting server certificate...")
            received_cert = client.utils.get(f"https://{address}/cert", verify=False)
            received_cert_hash = crypto_utils.hash(received_cert.encode()).hex()

            if not received_cert_hash == certificate_hash:
                raise Exception(
                    f"Hash of received server certificate not equals given hash. ({received_cert_hash} != {certificate_hash})"
                )

            cert_path = f"{client.path.user_data_dir}/{client.utils.address_to_key_path(address)}"
            os.makedirs(os.path.dirname(cert_path), exist_ok=True)
            with open(
                cert_path,
                "w",
            ) as fout:
                fout.write(received_cert)

            output("Getting iterations count...")
            iterations = int(
                client.utils.get(f"https://{address}/iterations", verify=cert_path)
            )

            output("Checking password...")
            checksum = json.loads(
                client.utils.get(f"https://{address}/checksum", verify=cert_path)
            )

            hash = base64.b64encode(
                crypto_utils.hash_with_salt(
                    password=password,
                    salt=base64.b64decode(checksum["salt"]),
                    iterations=iterations,
                )
            ).decode()

            if not hash == checksum["hash"]:
                raise Exception(f"Incorrect password: {hash} != {checksum["hash"]}")

            output("Generating key...")
            salt = client.utils.get(
                f"https://{address}/salt", verify=cert_path
            ).encode()

            key = crypto_utils.hash_with_salt(password.encode(), salt, iterations)

            output("Saving server to database...")
            client.db.cursor.execute(
                """INSERT INTO servers (address, key) VALUES (?, ?)""",
                (
                    address,
                    key,
                ),
            )
            client.db.connection.commit()

            output(f"Server {address} successfully added to database!", color="green")
            return True
        except Exception as e:
            traceback.print_exc()
            output(f"Failed to adding server {address} to database: {e}", color="red")
            return False
