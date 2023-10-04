import os


def get_broker_url():
    server = os.environ["BROKER_SERVER"] if "BROKER_SERVER" in os.environ else None
    return f'amqp://rabbitmq:rabbitmq@{server}:5672' if server else 'amqp://rabbitmq:rabbitmq@localhost:5672'