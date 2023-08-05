import os
import configparser

class Util:

    def __init__(cfg_path):
        self.conf = configparser.ConfigParser()
        self.conf = conf.read(cfg_path)

    def get_env_value(self, key, section):
        return os.getenv("{}_{}".format(section, key), self.conf.get(section, key))

    def getSecondsSinceEpoch(self):
        return int(time.time())

    def getMillisecondsSinceEpoch(self):
        return int(1000 * self.getSecondsSinceEpoch())
