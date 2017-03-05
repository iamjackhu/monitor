import unittest
from monitor.service.dbsession import DBSessionManager
from monitor.service.config import ConfigManager

class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        self._session = DBSessionManager.instance().getSession()
        self._config = ConfigManager.instance().getConfig()

    def tearDown(self):
        self._session.remove()

    def testConfig(self):
        assert self._config.has_section("db")
