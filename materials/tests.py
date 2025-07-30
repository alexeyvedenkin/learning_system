from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonAPITests(TestCase):
    def setUp(self):
        # Создание пользователя и логин
        self.user = User.objects.create(
            email='test@example.com', password='testpass'  # Используйте create вместо create_user
        )
        self.user.set_password('testpass')  # Устанавливаем пароль
        self.user.save()  # Сохраняем пользователя

        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Создаем курс для урока
        self.course = Course.objects.create(name="Тестовый Курс", owner=self.user)

        # Создаем тестовые данные для урока
        self.lesson_data = {
            "title": "Тестовый Урок",
            "description": "Описание тестового урока",
            "theme": self.course,  # Добавляем курс
        }

    def test_create_lesson(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на создание урока
        response = self.client.post(reverse("materials:lessons_create"), self.lesson_data)

        # Проверка, что урок создан
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_retrieve_lesson(self):
        # Создаем урок. Обратите внимание, что теперь theme находится внутри lesson_data
        lesson = Lesson.objects.create(owner=self.user, theme=self.course, **self.lesson_data)

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на получение урока
        response = self.client.get(reverse("materials:lessons_retrieve", args=[lesson.id]))

        # Проверка, что данные урока возвращены
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], lesson.title)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)
        updated_data = {
            "title": "Обновленный Урок",
            "description": "Описание обновленного урока",
            "theme": self.course,
        }

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на обновление урока
        response = self.client.put(reverse("materials:lessons_update", args=[lesson.id]), updated_data)

        # Проверка, что урок обновлен
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, updated_data["title"])

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на удаление урока
        response = self.client.delete(reverse("materials:lessons_delete", args=[lesson.id]))

        # Проверка, что урок удален
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class CourseViewSetTests(APITestCase):

    def setUp(self):
        # Создание пользователя и логин
        self.user = User.objects.create(
            email='test@example.com', password='testpass'  # Используйте create вместо create_user
        )
        self.user.set_password('testpass')  # Устанавливаем пароль
        self.user.save()  # Сохраняем пользователя

        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Создание тестового курса
        self.course = Course.objects.create(
            name='Тестовый курс',
            owner=self.user
        )

    def test_create_course(self):
        url = reverse('materials:course-list')
        data = {
            'name': 'Тестовый курс',
            'description': 'Содержимое тестового курса',
            'preview': None  # Если нужно, добавьте URL к изображению
        }
        response = self.client.post(url, data, format='json')  # Отправка запроса на создание курса
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверка ответа 201

    def test_get_courses(self):
        # Тест на получение списка курсов
        Course.objects.create(name="Курс 1", owner=self.user)
        response = self.client.get("/api/courses/")  # Замените на реальный URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_course(self):
        # Тест на обновление курса
        course = Course.objects.create(name="Курс 1", owner=self.user)
        data = {"name": "Обновленный курс"}
        response = self.client.put(f"/api/courses/{course.id}/", data)  # Замените на реальный URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=course.id).name, "Обновленный курс")

    def test_delete_course(self):
        # Тест на удаление курса
        course = Course.objects.create(name="Курс 1", owner=self.user)
        response = self.client.delete(f"/api/courses/{course.id}/")  # Замените на реальный URL
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
