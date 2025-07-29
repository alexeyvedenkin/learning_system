from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from users.models import User
from materials.models import Course, Lesson


class LessonAPITests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()

        # Создаем курс для урока
        self.course = Course.objects.create(name='Тестовый Курс', owner=self.user)

        # Создаем тестовые данные для урока
        self.lesson_data = {
            'title': 'Тестовый Урок',
            'theme': self.course.id,
            'description': 'Описание тестового урока'
        }

    def test_create_lesson(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на создание урока
        response = self.client.post(reverse('lesson-list'), self.lesson_data)

        # Проверка, что урок создан
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_retrieve_lesson(self):
        # Создаем урок
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на получение урока
        response = self.client.get(reverse('lesson-detail', args=[lesson.id]))

        # Проверка, что данные урока возвращены
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], lesson.title)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)
        updated_data = {'title': 'Обновленный Урок'}

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на обновление урока
        response = self.client.put(reverse('lesson-detail', args=[lesson.id]), updated_data)

        # Проверка, что урок обновлен
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, updated_data['title'])

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, **self.lesson_data)

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на удаление урока
        response = self.client.delete(reverse('lesson-detail', args=[lesson.id]))

        # Проверка, что урок удален
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
