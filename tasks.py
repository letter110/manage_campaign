import time
from celery import Celery

app = Celery('tasks', backend='redis://localhost:6379/0',
             broker='redis://localhost:6379/0')


@app.task
def call(customer_phone_number: str, campaign_name: str, isStart: bool = True):
    time.sleep(3)
    if isStart:
        return 'Complete call {} to notify campaign {} is started'.format(customer_phone_number, campaign_name)

# celery -A tasks worker -l info -P gevent
