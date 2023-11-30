from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Django의 settings 모듈을 Celery 프로그램의 기본 설정 소스로 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sara_server.settings")

app = Celery("sara_server")

# 문자열을 사용하여 설정을 설정하면, worker가 자식 프로세스가 설정을 직접 읽을 수 있도록 합니다.
app.config_from_object("django.conf:settings", namespace="CELERY")

# 등록된 Django App Configs의 모든 celery 태스크를 자동으로 로드합니다.
app.autodiscover_tasks()
