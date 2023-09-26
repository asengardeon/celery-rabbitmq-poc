from celery import Celery
from flask import Flask

from application.broker.consts import get_broker_url
from application.client.client import send_as_task
from application.tasks.tasks import hello_task

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = get_broker_url()
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def index():
    return 'index'

@app.get('/newmessage')
def newmessage():
    connection = celery.broker_connection()
    send_as_task(connection, fun=hello_task, args=('Kombu',), kwargs={}, priority='high')
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)