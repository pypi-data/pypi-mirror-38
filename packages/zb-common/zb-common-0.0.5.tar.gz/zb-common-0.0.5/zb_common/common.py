import os
import uuid
import configparser

class Util:

    def __init__(self, cfg_path):
        self.conf = configparser.ConfigParser()
        self.conf.read(cfg_path)

    def get_env_value(self, key, section):
        return os.getenv("{}_{}".format(section, key), self.conf.get(section, key))

    def getSecondsSinceEpoch(self):
        return int(time.time())

    def getMillisecondsSinceEpoch(self):
        return int(1000 * self.getSecondsSinceEpoch())

    def get_random_id_32(self):
        return uuid.uuid4().hex
