from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Subscription, User
from materials.models import Course


class SubscriptionAPITestCase(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.course = Course.objects.create(title='Test Course')
        self.url_subscribe = reverse('subscription-list')  # URL для создания подписки
        self.url_unsubscribe = reverse('subscription-detail', kwargs={'course_id': self.course.id})

    def test_subscribe(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Отправляем запрос для подписки
        response = self.client.post(self.url_subscribe, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка успешного создания
        self.assertEqual(response.data['message'], 'Подписка добавлена')

    def test_subscribe_duplicate(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Подписка на курс
        self.client.post(self.url_subscribe, {'course_id': self.course.id})

        # Попробуем подписаться повторно
        response = self.client.post(self.url_subscribe, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка успешного запроса
        self.assertEqual(response.data['message'], 'Подписка уже существует')

    def test_unsubscribe(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем подписку
        self.client.post(self.url_subscribe, {'course_id': self.course.id})

        # Запрос на удаление подписки
        response = self.client.delete(self.url_unsubscribe)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверка успешного удаления

    def test_unsubscribe_not_found(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Попробуем удалить подписку, когда ее нет
        response = self.client.delete(self.url_unsubscribe)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Проверка на несуществующую подписку

    def test_unauthenticated_access(self):
        # Проверка доступа без аутентификации
        response = self.client.post(self.url_subscribe, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Доступ запрещен

        response = self.client.delete(self.url_unsubscribe)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Доступ запрещен
