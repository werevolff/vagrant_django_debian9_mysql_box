from __future__ import absolute_import
import os
from celery import Celery
import environ

env = environ.Env(
    MAIN_APP_NAME=(str, ''),
)
ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
environ.Env.read_env(os.path.join(ROOT, '.env'))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    env('MAIN_APP_NAME') + '.settings'
)

from django.conf import settings  # noqa

app = Celery(
    env('MAIN_APP_NAME')
)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    return 'Request: {0!r}'.format(self.request)
