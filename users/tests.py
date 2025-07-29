from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Subscription, User, Payment
from materials.models import Course, Lesson


class UserTests(APITestCase):

    def setUp(self):
        """ Создаем тестового пользователя перед каждым тестом """
        self.test_user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='Тест',
            last_name='Пользователь'
        )

    def test_create_user(self):
        """ Тестируем создание нового пользователя """
        url = reverse('user-list')  # Получаем URL для эндпоинта списка пользователей
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'Новый',
            'last_name': 'Пользователь'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем, что статус 201 (Создано)

    def test_list_users(self):
        """ Тестируем получение списка пользователей """
        url = reverse('user-list')  # Получаем URL для списка пользователей
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Проверяем, что доступ закрыт для неавторизованных

    def test_retrieve_user(self):
        """ Тестируем получение пользовательских данных """
        url = reverse('user-detail', args=[self.test_user.id])  # URL для получения конкретного пользователя
        self.client.login(email='test@example.com', password='password123')  # Авторизуемся
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что статус 200 (Успех)

    def test_update_user(self):
        """ Тестируем обновление информации о пользователе """
        url = reverse('user-detail', args=[self.test_user.id])
        self.client.login(email='test@example.com', password='password123')
        data = {'first_name': 'Обновленный'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что статус 200

    def test_delete_user(self):
        """ Тестируем удаление пользователя """
        url = reverse('user-detail', args=[self.test_user.id])
        self.client.login(email='test@example.com', password='password123')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверяем, что статус 204 (Нет содержимого)


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


class PaymentTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Создаем тестовые объекты курса и урока
        self.course = Course.objects.create(title='Тестовый курс')
        self.lesson = Lesson.objects.create(title='Тестовый урок', course=self.course)
        # Создаем платёж
        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            lesson=self.lesson,
            amount=100.00,
            payment_method='cash'
        )

    def test_create_payment(self):
        # URL для создания платежа
        url = reverse('payment-create')
        data = {
            'user': self.user.id,
            'course': self.course.id,
            'lesson': self.lesson.id,
            'amount': 150.00,
            'payment_method': 'transfer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем, что создание прошло успешно

    def test_list_payments(self):
        url = reverse('payment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что список доступен

    def test_update_payment(self):
        url = reverse('payment-update', args=[self.payment.id])
        data = {
            'amount': 200.00,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что обновление прошло успешно

    def test_delete_payment(self):
        url = reverse('payment-destroy', args=[self.payment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверяем, что удаление прошло успешно
