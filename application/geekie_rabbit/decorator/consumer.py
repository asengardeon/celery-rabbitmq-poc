from concurrent.futures import ThreadPoolExecutor

from celery.beat import logger
from kombu.mixins import ConsumerMixin
from kombu.utils import reprcall

from application.broker.celery_configs import GT_Broker
from application.tasks.tasks import MyException

broker = GT_Broker('worker')

class Worker(ConsumerMixin):

    def __init__(self, connection, task_queues):
        self.connection = connection
        self.task_queues = task_queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.task_queues,
                         accept=['pickle', 'json'],
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        fun = body['fun']
        args = body['args']
        kwargs = body['kwargs']
        logger.info('Got task: %s', reprcall(fun.__name__, args, kwargs))
        try:
            fun(*args, **kwargs)
            message.ack()
        except MyException as exc:
            message.requeue()


def run_worker(broker_connection, task_queues):
    logger.info(f"trying to connect to: {broker_connection}")
    try:
        worker = Worker(broker_connection, task_queues)
        worker.run()

    except KeyboardInterrupt:
        print('bye bye')


def consumer(fun, task_queues=[]):
    def wrapper():
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = []
            for x in range(0, 1):
                futures.append(executor.submit(run_worker, broker.get_celery_broker().broker_connection(), task_queues))
    return wrapper