import json
import os.path


class Config:
    _data = {}

    @classmethod
    def load(cls):
        config_path = os.path.join(os.path.abspath(os.path.dirname(
            os.path.realpath(__file__))),
            "config.json")

        with open(config_path, "r") as config_file:
            cls._data = json.load(config_file)

    @classmethod
    def get(cls, key: str):
        return cls._data.get(key, None)
