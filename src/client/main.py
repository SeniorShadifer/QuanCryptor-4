import webview
from termcolor import colored

import client.Api
import client.const
import client.path
from common import utils


def main():
    print(colored(f"{client.const.APP_FULLNAME}", color="green"))

    api = client.Api.Api()
    window = webview.create_window(
        title=f"{client.const.APP_FULLNAME} WebGUI",
        url=f"file:///{client.path.absolute_application_path}/index.html",
        js_api=api,
        min_size=(500, 250),
    )
    webview.start()
