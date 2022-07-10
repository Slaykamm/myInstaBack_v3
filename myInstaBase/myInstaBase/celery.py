import os
from celery import Celery
from celery.schedules import crontab

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myInstaBase.settings')
 
app = Celery('myInstaBase')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send userEmails': {
        'task': 'storage.tasks.sendDaylyEmails',
        'schedule': crontab(minute='*/1'),
        'args': (),
    },
}
