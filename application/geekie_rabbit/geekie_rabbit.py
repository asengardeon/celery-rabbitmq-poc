from functools import wraps, partial
from typing import List

from kombu import Queue, Exchange
from kombu.common import logger

from app import broker
from application.geekie_rabbit.worker import Worker


class GeekieQueueExchange():
    def __init__(self, name, exchange_name):
        self.name = name
        self.exchange_name = exchange_name

class GeekieRabbit():

    queues = {}
    callbacks = {}
    _prefix = ""
    def __init__(self, queue_exchanges: List[GeekieQueueExchange]):
        self.connection = broker.get_celery_broker().broker_connection()
        self.queue_exchanges = queue_exchanges
        self.init_queues()

    def init_queues(self, ):
        for q in self.queue_exchanges:
            name = q.name
            if name not in self.queues:
                self.queues[name] = []
            if name not in self.callbacks:
                self.callbacks[name] = []

            logger.debug("Setting up %s" % name)
            routing_key = "*"

            task_exchange = Exchange(f'{q.exchange_name}', type='topic')
            task_exchange_dlq = Exchange(f'{q.exchange_name}_dlq', type='topic')

            queue = Queue(name,
                          task_exchange,
                          routing_key=routing_key,
                          queue_arguments={'x-queue-type': 'quorum','x-dead-letter-exchange': f'{q.exchange_name}_dlq', 'x-delivery-limit': 10})

            queue.bind(self.connection).declare()

            queue_dlq = Queue(f'{name}_dlq',
                          task_exchange_dlq,
                          routing_key=routing_key,
                          queue_arguments={'x-queue-type': 'quorum'})

            queue_dlq.bind(self.connection).declare()

            self.queues[name].append(queue)


    def _wrap_function(self, function, callback, queue_name, task=False):

        self.callbacks[queue_name].append(callback)

        # The function returned by the decorator don't really do
        # anything.  The process_msg callback added to the consumer
        # is what actually responds to messages  from the client
        # on this particular queue.

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                pass
            return wrapper
        return decorate

    def task(self, func=None, *, queue_name=None):
        """Wrap around a function that should be a task.
        The client should not expect anything to be returned.

        """
        if func is None:
            return partial(self.task, queue_name=queue_name)

        def process_message(body, message):
            logger.debug("Processing function {!r} "
                         " in message: {!r} "
                         "with data {!r}".format(func.__name__,
                                                 message,
                                                 body))
            try:
                func(body)
            except Exception:
                logger.error("Problem processing task", exc_info=True)
            else:
                logger.debug("Ack'ing message.")
                message.ack()

        return self._wrap_function(
            func, process_message, queue_name, task=True)


    def run(self):
        try:
            worker = Worker(self.connection, self)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')