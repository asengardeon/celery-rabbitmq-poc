from celery import Celery, bootsteps
from kombu import Exchange, Queue

from application.broker.consts import get_broker_url
from application.broker.queues import queues_names

class GT_Broker:
    celery_broker = None

    def bind_queues(self):
        for name in queues_names:
            dlx = Exchange(f'dlq_{name}_exchange', type='topic')

            dead_letter_queue = Queue(f'dlq_{name}', dlx, routing_key='*')
            dead_letter_queue.bind(self.celery_broker.broker_connection()).declare()

    def __init__(self, app_name):
        self.celery_broker = Celery(app_name, broker=get_broker_url(), set_as_current=True)
        self.bind_queues()

    def get_celery_broker(self):
        return self.celery_broker