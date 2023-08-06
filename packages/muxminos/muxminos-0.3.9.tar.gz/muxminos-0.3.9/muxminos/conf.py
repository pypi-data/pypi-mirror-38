import os
import errno
import json
import yaml
from os.path import expanduser
from configobj import ConfigObj


class LocalConfig(object):
    def __init__(self):
        self.__config_path = os.path.join(
            os.path.expanduser("~"), ".config", "xiaomi", "config"
        )
        self.mkdirs(os.path.join(os.path.expanduser("~"), ".config", "xiaomi"))

        self.__data = None
        with open(self.__config_path) as f:
            self.__data = json.load(f)

    @property
    def xiaomi_username(self):
        return self.__data.get("xiaomi_username")

    @xiaomi_username.setter
    def xiaomi_username(self, value):
        if value is not None and value.strip() != "":
            self.__data["xiaomi_username"] = value
            self.dump()

    @property
    def minos1_config_location(self):
        return self.__data.get("minos1_config_location")

    @minos1_config_location.setter
    def minos1_config_location(self, value):
        if value is not None and value.strip() != "":
            self.__data["minos1_config_location"] = value
            self.dump()

    @property
    def minos2_config_location(self):
        return self.__data.get("minos2_config_location")

    @minos2_config_location.setter
    def minos2_config_location(self, value):
        if value is not None and value.strip() != "":
            self.__data["minos2_config_location"] = value
            self.dump()

    def dump(self):
        with open(self.__config_path, "w") as outfile:
            json.dump(
                self.__data, outfile, sort_keys=True, indent=4, separators=(",", ": ")
            )

    def mkdirs(self, path):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(
                os.path.join(os.path.expanduser("~"), ".config", "xiaomi")
            ):
                pass
