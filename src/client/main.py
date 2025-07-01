import webview
from webview import guilib

import client.Api, client.const, client.path
from common import os_utils


def main():
    (
        client.path.user_data_dir,
        client.path.user_cache_dir,
        client.path.user_config_dir,
    ) = os_utils.create_and_get_platform_dirs(
        app_name=client.const.APP_NAME,
        app_author=client.const.APP_AUTHOR,
        app_version=client.const.APP_VERSION,
    )

    client.db.prepare_database()

    window = webview.create_window(
        title=f"{client.const.APP_FULLNAME} WebGUI",
        url=f"file:///{client.path.absolute_application_path}/index.html",
        js_api=client.Api.Api(),
        min_size=(500, 250),
        background_color="#000000",
    )
    webview.start(ssl=True, icon=f"{client.path.absolute_application_path}/favicon.png")
