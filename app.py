from flask import Flask, request
from hijiki.publisher.Publisher import Publisher

from application.broker.celery_configs import GT_Broker
from application.client.client import send_as_task_v1, publish_message
from application.tasks.tasks import hello_task

app = Flask(__name__)
broker = GT_Broker('client')

@app.route('/')
def index():
    return 'index'

@app.get('/newmessage')
def newmessage():
    val = request.args.get('value')
    val = 'Kombu' if not val else val
    connection = broker.get_celery_broker().broker_connection()
    send_as_task_v1(connection, fun=hello_task, args=(val,), kwargs={}, priority='high')
    return "OK"


@app.get('/publish_message')
def send_message():
    pub = Publisher("localhost", "user", "pwd", 5672)
    pub.publish_message('teste1_event', '{"value": "Esta é a mensagem"}')
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)