import json
import os

from platformdirs import user_data_dir, user_cache_dir, user_config_dir


def create_and_get_platform_dirs(app_name: str, app_author: str, app_version: str):
    data_dir = user_data_dir(
        appname=app_name,
        appauthor=app_author,
        version=app_version,
    )

    cache_dir = user_cache_dir(
        appname=app_name,
        appauthor=app_author,
        version=app_version,
    )

    config_dir = user_config_dir(
        appname=app_name,
        appauthor=app_author,
        version=app_version,
    )

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return data_dir, cache_dir, config_dir


def load_configuration(path: str, default={}):
    ret = {}
    if os.path.exists(path):
        with open(path, "r") as fin:
            ret = json.loads(fin.read())

        for key, value in default.items():
            if key not in ret:
                ret[key] = value

        with open(path, "w") as fout:
            fout.write(json.dumps(ret))
    else:
        with open(path, "w") as fout:
            fout.write(json.dumps(default))
            ret = default

    return ret


def load_or_generate_bytes(path: str, len: int = 16):
    ret: bytes
    if os.path.exists(path):
        with open(path, "r") as fin:
            ret = fin.read().encode()
    else:
        ret = os.urandom(len).hex().encode()
        with open(path, "w") as fout:
            fout.write(ret.decode())

    return ret
