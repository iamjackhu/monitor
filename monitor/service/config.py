from monitor.service.singleton import SingletonMixin
from ConfigParser import SafeConfigParser

import os

class ConfigManager(SingletonMixin):

    def __init__(self):
        app_home = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_file = os.path.join(app_home, "config.ini")
        self._config = SafeConfigParser()
        self._config.read(config_file)

    def getConfig(self):
        return self._config