from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from task_manager import tasks

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_task_manager.settings')
app = Celery('employee_task_manager')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=00, day_of_week=6),
        execute_every_saturday.s(),
    )
    sender.add_periodic_task(crontab(minute='*/2'), execute_everyminutes.s(),)
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
@app.task
def execute_every_saturday():
    tasks.weekly_task_report_of_employers()

# @app.task
# def execute_everyminutes():
#     """for testing """
#     tasks.weekly_task_report_of_employers()