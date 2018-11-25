
import os.path
import json
import logging

CONFIG_FILE_PATH = "netpify.conf"

DEFAULT_CONFIG = {
    "location": "espol",
    "name": "medidor1",
    "id": 1234,
    "mode": "single_phase",
    "voltage_source_1": "L1",
    "time_interval": 300
}

config = {}


def read():

    global config
    if not os.path.isfile(CONFIG_FILE_PATH):
        logging.warning("config file '%s' not found, using default config", CONFIG_FILE_PATH)
        config = DEFAULT_CONFIG

    logging.debug("opening '%s'", CONFIG_FILE_PATH)
    with open(CONFIG_FILE_PATH, "r") as f:
        config = json.load(f)


def write(config_dict):
    global config
    config = config_dict
    with open(CONFIG_FILE_PATH, "w") as write_file:
        json.dump(config, write_file)