from monitor.service.singleton import SingletonMixin
from apscheduler.schedulers.background import BackgroundScheduler

class SchedulerManager(SingletonMixin):

    def __init__(self):
        self._scheduler = BackgroundScheduler()

    def start(self, db_url):
        self._scheduler.add_jobstore('sqlalchemy',db_url)
        self._scheduler.start()

    def stutdown(self):
        self._scheduler.shutdown()

    def add_interval_job(self, func, args, seconds = 60):
        self._scheduler.add_job(func, 'interval', args, seconds)

    def add_cron_job(self, func, hour, minute):
        self._scheduler.add_job(func, 'cron', hour, minute)