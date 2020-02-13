# celery相关配置

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','M_community.settings')
app = Celery('M_community')
app.conf.update(
    BROKER_URL = 'redis://:lishuo007@127.0.0.1:6379/1',
)

# celery 自动去该参数位置寻找worker任务
app.autodiscover_tasks(settings.INSTALLED_APPS)