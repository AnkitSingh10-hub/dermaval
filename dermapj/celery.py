import os

from celery import Celery
from decouple import config
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dermapj.settings")

app = Celery(
    "dermapj ", backend=settings.CELERY_RESULT_BACKEND, broker=settings.BROKER_URL
)
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Default queue name for this app
# Changed to make sure other app's queue does not collide
# Make sure to add -Q 'queue_name' to celery worker command
app.conf.task_default_queue = config(
    "TASK_DEFAULT_QUEUE", default="geokrishi", cast=str
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
task = app.task
