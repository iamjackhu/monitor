from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from monitor.service.singleton import SingletonMixin
from monitor.service.config import ConfigManager

class DBSessionManager(SingletonMixin):

    def __init__(self):
        config = ConfigManager.instance().getConfig()
        db_url = config.get("db","db_url")
        engine = create_engine(db_url)
        session_factory = sessionmaker(bind=engine)
        self._session = scoped_session(session_factory)  # thread local

    def getSession(self):
        return self._session