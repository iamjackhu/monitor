import sys

from monitor.service.dbsession import DBSessionManager
from monitor.service.config import ConfigManager

if __name__ == '__main__':
    import sys
    sys = reload(sys)
    sys.setdefaultencoding("utf-8")

    print ConfigManager.instance().getConfig().has_section("db")

