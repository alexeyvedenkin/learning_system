from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Добавляет новый платеж в таблицу Payment'

    def handle(self, *args, **kwargs):
        # Получаем существующего пользователя по email
        user_email = input('Введите email пользователя: ')
        user = User.objects.filter(email=user_email).first()

        if not user:
            self.stdout.write(self.style.ERROR('Пользователь не найден.'))
            return

        # Получаем курс и урок
        course = Course.objects.first()  # Получаем первый курс, можно изменить логику
        lesson = Lesson.objects.first()  # Получаем первый урок, можно изменить логику

        if not course or not lesson:
            self.stdout.write(self.style.ERROR('Курс или урок не найдены.'))
            return

        # Сумма и способ оплаты
        amount = input('Введите сумму оплаты: ')
        payment_method = input('Введите способ оплаты (cash или transfer): ')

        # Создаем новый платеж
        Payment.objects.create(
            user=user,
            course=course,
            lesson=lesson,
            amount=amount,
            payment_method=payment_method,
        )

        self.stdout.write(self.style.SUCCESS('Платеж успешно добавлен.'))
