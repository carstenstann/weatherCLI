import configparser
import pathlib
import sys

from weathercli import __app_name__


CONFIG_FILENAME = 'config.ini'


def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """
    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


def get_app_dir():
    # create your program's directory
    return get_datadir() / __app_name__


def get_config_path():
    return get_app_dir() / CONFIG_FILENAME


def init_config_file():
    config_file_dir = get_app_dir()
    config_file_path = get_config_path()

    try:
        config_file_dir.mkdir(exist_ok=True)
    except OSError:
        print("config directory error")
        sys.exit(1)
    
    try:
        config_file_path.touch(exist_ok=True)
    except OSError:
        print("config file error")
        sys.exit(1)

    return config_file_path


def get_config():
    config_file_path = get_config_path()
    if not config_file_path.is_file():
        raise FileNotFoundError
    
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def set_api_key(key):
    config_file_path = init_config_file()

    config = configparser.ConfigParser()
    config.read(config_file_path)
    config['openweather'] = {'api_key': key}

    try:
        with config_file_path.open("w") as configfile:
            config.write(configfile)
    except OSError:
            print("config file error")
