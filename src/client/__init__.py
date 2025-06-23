import os

from platformdirs import user_data_dir, user_config_dir, user_cache_dir

import client.const
import client.path


client.path.absolute_application_path = os.path.dirname(os.path.abspath(__file__))


client.path.user_data_dir = user_data_dir(
    appname=client.const.APP_NAME,
    appauthor=client.const.APP_AUTHOR,
    version=client.const.APP_VERSION,
)

client.path.user_cache_dir = user_cache_dir(
    appname=client.const.APP_NAME,
    appauthor=client.const.APP_AUTHOR,
    version=client.const.APP_VERSION,
)

client.path.user_config_dir = user_config_dir(
    appname=client.const.APP_NAME,
    appauthor=client.const.APP_AUTHOR,
    version=client.const.APP_VERSION,
)

if not os.path.exists(client.path.user_data_dir):
    os.makedirs(client.path.user_data_dir)

if not os.path.exists(client.path.user_cache_dir):
    os.makedirs(client.path.user_cache_dir)

if not os.path.exists(client.path.user_config_dir):
    os.makedirs(client.path.user_config_dir)
