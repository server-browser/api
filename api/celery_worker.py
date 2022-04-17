import os
import time

from celery import Celery
from celery.schedules import crontab

from api.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
celery.conf.timezone = 'UTC'

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from api.worker.server_info import update_all
    sender.add_periodic_task(10.0, update_all, name='add every 10')
