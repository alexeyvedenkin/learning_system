from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def deactivate_inactive_users():
    """ Деактивирует пользователей, не заходивших более месяца """
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False  # Блокируем пользователя
        user.save()  # Сохраняем изменения в базе данных
