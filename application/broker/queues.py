from kombu import Exchange, Queue

queues_names = ['hipri', 'midpri', 'lopri' ]

task_exchange = Exchange('tasks', type='topic')

task_queues = [Queue(name, task_exchange, routing_key=name, queue_arguments={'x-queue-type': 'quorum', 'x-dead-letter-exchange': f'dql_{name}', 'x-dead-letter-routing-key': f'dql_{name}'}) for name in queues_names]




