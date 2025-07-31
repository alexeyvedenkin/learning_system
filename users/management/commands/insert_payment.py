from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Добавляет новый платеж в таблицу Payment"

    def handle(self, *args, **kwargs):
        # Получаем существующего пользователя по email
        user_email = input("Введите email пользователя: ")
        user = User.objects.filter(email=user_email).first()

        if not user:
            self.stdout.write(self.style.ERROR("Пользователь не найден."))
            return

        # Получаем все курсы и выводим их для выбора
        courses = Course.objects.all()
        if not courses:
            self.stdout.write(self.style.ERROR("Нет доступных курсов."))
            return

        self.stdout.write("Доступные курсы:")
        for i, course in enumerate(courses, 1):
            self.stdout.write(f"{i}. {course.name}")  # Выводим названия курсов

        # Запрашиваем, будет ли оплата за курс или за урок
        payment_type = input('Платеж за курс или урок? (введите "курс" или "урок"): ').strip().lower()

        if payment_type == "курс":
            course_index = int(input("Выберите курс по номеру: ")) - 1
            course = courses[course_index]

            # Получаем все уроки, связанные с выбранным курсом
            lessons = Lesson.objects.filter(theme=course)
            if lessons:
                for lesson in lessons:
                    lesson.paid = True  # Отмечаем все уроки как оплаченные
            else:
                self.stdout.write(self.style.ERROR("Нет доступных уроков для этого курса."))
                return

        elif payment_type == "урок":
            lesson_index = int(input("Введите номер урока из доступных: ")) - 1
            lesson = Lesson.objects.all()[lesson_index]  # Получаем урок без привязки к курсу
            course = None  # Урок не привязан к курсу

        else:
            self.stdout.write(self.style.ERROR("Некорректный ввод типа платежа."))
            return

        # Сумма и способ оплаты
        amount = input("Введите сумму оплаты: ")
        payment_method = input("Введите способ оплаты (cash или transfer): ")

        # Создаем новый платеж
        Payment.objects.create(
            user=user,
            course=course,  # Здесь может быть None для отдельных уроков
            lesson=lesson,
            amount=amount,
            payment_method=payment_method,
        )

        self.stdout.write(self.style.SUCCESS("Платеж успешно добавлен."))
