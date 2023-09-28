from celery import Celery, bootsteps
from kombu import Exchange, Queue

from application.broker.consts import get_broker_url
from application.broker.queues import queues_names


class DeclareDLXnDLQ(bootsteps.StartStopStep):
    """
    Celery Bootstep to declare the DL exchange and queues before the worker starts
        processing tasks
    """
    requires = {'celery.worker.components:Pool'}

    def start(self, worker):
        app = worker.app

        for name in queues_names:
            dlx = Exchange(name, type='direct')

            dead_letter_queue = Queue(
                f'dql_{name}', dlx, routing_key=f'dql_{name}')

            with worker.app.pool.acquire() as conn:
                dead_letter_queue.bind(conn).declare()


class GT_Broker:
    celery_broker = None

    def __init__(self, app_name):
        self.celery_broker = Celery(app_name, broker=get_broker_url(), set_as_current=True)
        self.celery_broker.steps['worker'].add(DeclareDLXnDLQ)
    def get_celery_broker(self):
        return self.celery_broker