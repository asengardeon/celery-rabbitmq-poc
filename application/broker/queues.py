from kombu import Exchange, Queue

queues_names = ['my_tasks_queue']

task_exchange = Exchange('tasks', type='topic')

task_queues = [Queue(name, task_exchange, routing_key='*', queue_arguments={'x-queue-type': 'quorum','x-dead-letter-exchange': f'dlq_{name}_exchange', 'x-delivery-limit': 10}) for name in queues_names]




