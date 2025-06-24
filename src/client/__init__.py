import os

from platformdirs import user_data_dir, user_config_dir, user_cache_dir
from termcolor import colored

import client.const
import client.path
from common import os_utils


print(colored(f"{client.const.APP_FULLNAME}", color="green"))


client.path.absolute_application_path = os.path.dirname(os.path.abspath(__file__))

client.path.user_data_dir, client.path.user_cache_dir, client.path.user_config_dir = (
    os_utils.create_and_get_platform_dirs(
        app_name=client.const.APP_NAME,
        app_author=client.const.APP_AUTHOR,
        app_version=client.const.APP_VERSION,
    )
)
