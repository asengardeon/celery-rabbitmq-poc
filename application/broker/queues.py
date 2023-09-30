from kombu import Exchange, Queue

queues_names = ['hipri', 'midpri', 'lopri' ]

task_exchange = Exchange('tasks', type='topic')

task_queues = [Queue(name, task_exchange, routing_key=name, queue_arguments={'x-queue-type': 'quorum', 'x-dead-letter-exchange': f'dlq_{name}_exchange', 'x-dead-letter-routing-key': f'dlq_{name}_exchange', 'x-dead-letter-strategy': 'at-least-once', 'overflow': 'reject-publish'}, ) for name in queues_names]




