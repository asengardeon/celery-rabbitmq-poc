from kombu import Exchange, Queue

queues_names = ['my_tasks_queue']

task_exchange = Exchange('tasks', type='fanout')

task_queues = [Queue(name, task_exchange, routing_key=name, queue_arguments={'x-dead-letter-exchange': f'dlq_{name}_exchange'}) for name in queues_names]




