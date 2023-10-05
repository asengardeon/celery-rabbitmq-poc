from application.geekie_rabbit.geekie_rabbit import GeekieRabbit, GeekieQueueExchange

qs = [GeekieQueueExchange('teste1', 'teste1_event'), GeekieQueueExchange('teste2', 'teste2_event')]
gr = GeekieRabbit(qs)

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
