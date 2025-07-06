# app/utils/email_tasks.py

from app.celery_worker import celery_app
from app.utils.email_service import email_service

@celery_app.task(name="app.utils.email_tasks.send_welcome_email_task")
def send_welcome_email_task(to_email, username):
    # your email sending logic
    email_service.send_welcome_email(to_email=to_email, username=username)
    print(f"Sending welcome email to {to_email}, username={username}")
