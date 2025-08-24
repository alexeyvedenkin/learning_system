import os

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(email_list, course_name):
    """ Отправляет уведомление об обновлении курса """
    subject = f"Обновление курса: {course_name}"
    message = f"Курс '{course_name}' был обновлён. Проверьте его!"
    send_mail(subject, message, from_email=os.getenv("FROM_EMAIL"), recipient_list=email_list)


@shared_task
def send_lesson_update_email(email_list, lesson_name):
    """ Отправляет уведомление об обновлении урока """
    subject = f"Обновление урока: {lesson_name}"
    message = f"Урок '{lesson_name}' был обновлён. Проверьте его!"
    send_mail(subject, message, from_email=os.getenv("FROM_EMAIL"), recipient_list=email_list)
