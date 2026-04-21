"""Configuracao da aplicacao Celery do servico Fantasy.

Define broker/backend Redis e registra tasks assincronas.
"""

import os
from celery import Celery

redis_url = os.getenv("REDIS_URL")
celery_app = Celery("fantasy_worker", broker=redis_url, backend=redis_url, include=['tasks'])

celery_app.conf.timezone = 'UTC'
