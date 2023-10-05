from kombu import producers, Exchange

from application.broker.queues import task_exchange

priority_to_routing_key = {
    'high': 'hipri',
    'mid': 'midpri',
    'low': 'lopri',
}


def send_as_task_v1(connection, fun, args=(), kwargs={}, priority='mid'):
    payload = {'fun': fun, 'args': args, 'kwargs': kwargs}
    routing_key = priority_to_routing_key[priority]

    with producers[connection].acquire(block=True) as producer:
        producer.publish(payload,
                         serializer='pickle',
                         compression='bzip2',
                         exchange=task_exchange,
                         declare=[task_exchange],
                         routing_key=routing_key)

def publish_message(connection, data: str, event_name):
    payload = {"value": data}

    with producers[connection].acquire(block=True) as producer:
        task_exchange = Exchange(event_name, type='topic')
        producer.publish(payload,  exchange=task_exchange, declare=[task_exchange], routing_key='x')

