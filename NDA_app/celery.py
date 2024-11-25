from __future__ import absolute_import, unicode_literals
import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nda.settings')

app = Celery('nda')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False

app.conf.update(timezone=os.getenv('TIMEZONE'))

app.autodiscover_tasks()