"""Configuracao Celery do servico de Heuristica.

Registra worker em tempo real e tarefas agendadas (Celery Beat).
"""

import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "heuristics_worker", 
    broker=os.getenv("REDIS_URL"), 
    backend=os.getenv("REDIS_URL"),
    include=['worker', 'tasks']
)

celery_app.conf.timezone = 'UTC'
celery_app.conf.beat_schedule = {
    'analise-z-score-madrugada': {
        'task': 'tasks.analyze_global_deviations',
        'schedule': crontab(hour=4, minute=0),
    },
}
