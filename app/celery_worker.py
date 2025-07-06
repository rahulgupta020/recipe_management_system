# app/celery_worker.py

from celery import Celery

celery_app = Celery(
    "myapp",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://"
)

celery_app.autodiscover_tasks([
    "app.utils",
])

from app.utils import email_tasks



# run this on cmd
# >celery -A app.celery_worker worker --loglevel=info --pool=solo