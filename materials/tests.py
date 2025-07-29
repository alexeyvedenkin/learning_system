from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonAPITests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # Создаем курс для урока
        self.course = Course.objects.create(name="Тестовый Курс", owner=self.user)

        # Создаем тестовые данные для урока
        self.lesson_data = {
            "title": "Тестовый Урок",
            "theme": self.course.id,
            "description": "Описание тестового урока",
        }

    def test_create_lesson(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на создание урока
        response = self.client.post(reverse("lesson-list"), self.lesson_data)

        # Проверка, что урок создан
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_retrieve_lesson(self):
        # Создаем урок
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на получение урока
        response = self.client.get(reverse("lesson-detail", args=[lesson.id]))

        # Проверка, что данные урока возвращены
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], lesson.title)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)
        updated_data = {"title": "Обновленный Урок"}

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на обновление урока
        response = self.client.put(reverse("lesson-detail", args=[lesson.id]), updated_data)

        # Проверка, что урок обновлен
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, updated_data["title"])

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на удаление урока
        response = self.client.delete(reverse("lesson-detail", args=[lesson.id]))

        # Проверка, что урок удален
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class CourseViewSetTests(APITestCase):

    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_create_course(self):
        # Тест на создание курса
        data = {"name": "Тестовый курс", "description": "Описание тестового курса"}
        response = self.client.post("/api/courses/", data)  # Замените на реальный URL вашего эндпоинта
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, "Тестовый курс")

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
