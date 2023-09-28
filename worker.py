import asyncio
import concurrent

from celery.exceptions import Reject
from kombu.mixins import ConsumerMixin, logger
from kombu.utils import reprcall

from application.broker.celery_configs import GT_Broker
from application.broker.queues import task_queues


class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=task_queues,
                         accept=['pickle', 'json'],
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        fun = body['fun']
        args = body['args']
        kwargs = body['kwargs']
        logger.info('Got task: %s', reprcall(fun.__name__, args, kwargs))
        try:
            fun(*args, **kwargs)
        except Exception as exc:
            message.reject(requeue=True)
        message.ack()

def run_worker(broker_connection):
    logger.info(f"trying to connect to: {broker_connection}")
    try:
        worker = Worker(broker_connection)
        worker.run()

    except KeyboardInterrupt:
        print('bye bye')
def main():
    from kombu.utils.debug import setup_logging

    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])
    broker = GT_Broker('worker')
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for x in range(0, 1):
            futures.append(executor.submit(run_worker, broker.get_celery_broker().broker_connection()))


if __name__ == '__main__':
    main()

