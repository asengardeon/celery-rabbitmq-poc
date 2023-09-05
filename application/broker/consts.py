import os


def get_broker_url():
    server = os.environ["BROKER_SERVER"] if "BROKER_SERVER" in os.environ else None
    return f'amqp://admin:mypass@{server}:5672' if server else 'amqp://admin:mypass@localhost:5672'