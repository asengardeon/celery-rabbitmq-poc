from celery import Celery

from application.broker.consts import get_broker_url

class GT_Broker:
    celery_broker = None

    def __init__(self, app_name):
        self.celery_broker = Celery(app_name, broker=get_broker_url(), set_as_current=True)
    def get_celery_broker(self):
        return self.celery_broker