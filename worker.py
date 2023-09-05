from kombu.mixins import ConsumerMixin, logger
from kombu.utils import reprcall

from application.broker.consts import get_broker_url
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
            logger.error('task raised exception: %r', exc)
        message.ack()

if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging

    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])
    broker_url = get_broker_url()
    logger.info(f"trying to connect to: {broker_url}")
    with Connection(broker_url) as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')