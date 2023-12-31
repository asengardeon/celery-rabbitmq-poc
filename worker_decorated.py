from hijiki.broker.hijiki_rabbit import HijikiQueueExchange, HijikiRabbit

qs = [HijikiQueueExchange('teste1', 'teste1_event'), HijikiQueueExchange('teste2', 'teste2_event')]
gr = HijikiRabbit().with_queues_exchange(qs).with_username("rabbitmq") \
        .with_password("rabbitmq") \
        .with_host("localhost") \
        .with_port(5672) \
        .build()

class MeuConsumidor():
    @gr.task(queue_name='teste1')
    def meu_consumidor(self):
        print("consumidor1 executado")

    @gr.task(queue_name='teste2')
    def meu_consumidor2(self):
        print("consumidor2 executado")

if __name__ == '__main__':
    MeuConsumidor()
    gr.run()
