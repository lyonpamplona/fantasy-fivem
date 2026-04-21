"""Fabrica da aplicacao Celery vinculada ao broker/backend Redis."""

import os

from celery import Celery

redis_url = os.getenv("REDIS_URL")

celery_app = Celery("fantasy_worker", broker=redis_url, backend=redis_url, include=['tasks'])
