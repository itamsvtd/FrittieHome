from celery.task import PeriodicTask
from frittie.app.main.cron_job import test
from datetime import timedelta


class SendEmailTask(PeriodicTask):
    run_every = timedelta(minutes=1)

    def run(self, **kwargs):
        test()