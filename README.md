# POC celery + Rabbit
Projeto com objetivo para testar a integração celery + rabbit para s=publish subscriber.

## Depdendencias:
- pyhton 3.11
- pipenv. Este projeto utiliza pipenv(https://pipenv.pypa.io/en/latest/) como gerenciador de dependencias. 
Para instalar o Pipenv
```shell
pip install pipenv
```

Após é executar:
```shell
pipenv install
```

## Arquivos principais
- app : aplicação flask para publicar mensagem
- worker : aplicaçãoque fica escutando fila para processar as mensagens


## executando
Este projeto possui um arquivo docker-compose que inicia o rabbit, aplicação worker(consumidora) e um publisher escrito com Flask.
para exeuctar é necessário apenas executar o comando :
```shell
docker-compose up --build
```

## Testando
A aplicação para publicar iniciará na no endereço http://127.0.0.1:5000. 
O endereço http://127.0.0.1:5000/newmessage publicará uma mensagem por topico que será consumida pela fila que o worker estará atuando:

## Logs exemplos:
```
Connected to amqp://admin:**@rabbitmq:5672//
2023-09-05T14:03:32.225804622Z 172.26.0.1 - - [05/Sep/2023 14:03:32] "GET / HTTP/1.1" 200 -
2023-09-05T14:03:37.079825081Z 172.26.0.1 - - [05/Sep/2023 14:03:37] "GET /newmessage HTTP/1.1" 200 -
2023-09-05T14:03:37.097838886Z Got task: hello_task('Kombu')
```
