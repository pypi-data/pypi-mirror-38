import os, sys
import yaml

config = None


def set_config():
    environment_config = _get_environment_config()
    global config
    if config is None:
        config = _load_yaml_config(environment_config)


def get_config(key):
    """ 
    Gets config value

    :param: key: config value key

    :returns: config value
    """
    return config[key]


def _get_environment_config():
    environment = os.environ.get("environment", "")
    config_filename = f"config/config.{environment}.yml"
    return config_filename


def _load_yaml_config(config_file_name):
    with open(config_file_name, "r") as f:
        return yaml.load(f)
