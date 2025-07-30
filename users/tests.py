from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from materials.models import Course, Lesson

from .models import Payment, Subscription, User


class UserTests(APITestCase):

    def setUp(self):
        """Создаем тестового пользователя перед каждым тестом"""
        self.test_user = User.objects.create_user(
            email="test@example.com", password="password123", first_name="Тест", last_name="Пользователь"
        )

    def test_create_user(self):
        """Тестируем создание нового пользователя"""
        url = reverse("users:user-list")  # Получаем URL для эндпоинта списка пользователей
        data = {
            "email": "new_user@example.com",
            "password": "password123",
            "first_name": "Новый",
            "last_name": "Пользователь",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем, что статус 201 (Создано)

        self.assertTrue(User.objects.filter(email="new_user@example.com").exists())

    def test_list_users(self):
        """Тестируем получение списка пользователей"""
        # Получаем токен для аутентификации
        # refresh = RefreshToken.for_user(self.test_user)
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')  # Устанавливаем токен в заголовок

        url = reverse("users:user-list")  # Получаем URL для списка пользователей
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Проверяем, что доступ закрыт для неавторизованных

    def test_retrieve_user(self):
        """Тестируем получение пользовательских данных"""
        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')  # Устанавливаем токен в заголовок

        url = reverse("users:user-detail", args=[self.test_user.id])  # URL для получения конкретного пользователя
        self.client.login(email="test@example.com", password="password123")  # Авторизуемся
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что статус 200 (Успех)

    def test_update_user(self):
        """Тестируем обновление информации о пользователе"""
        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')  # Устанавливаем токен в заголовок

        url = reverse("users:user-detail", args=[self.test_user.id])
        self.client.login(email="test@example.com", password="password123")
        data = {"first_name": "Обновленный"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что статус 200

    def test_delete_user(self):
        """Тестируем удаление пользователя"""
        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')  # Устанавливаем токен в заголовок

        url = reverse("users:user-detail", args=[self.test_user.id])
        self.client.login(email="test@example.com", password="password123")
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )  # Проверяем, что статус 204 (Нет содержимого)

    def test_get_user_list(self):
        """Тест для получения списка пользователей."""
        # Получение URL для списка пользователей
        url = reverse('users:user-list')  # Используем имя маршрута
        response = self.client.get(url)  # Отправляем GET-запрос на URL списком пользователей
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что статус ответа 200 (OK)
        self.assertGreater(len(response.data), 0)  # Проверяем, что список пользователей не пустой


class SubscriptionAPITestCase(TestCase):

    def setUp(self):
        # Создание пользователя и логин
        self.user = User.objects.create(
            email='test@example.com', password='testpass'  # Используйте create вместо create_user
        )
        self.user.set_password('testpass')  # Устанавливаем пароль
        self.user.save()  # Сохраняем пользователя

        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.course = Course.objects.create(name="Test Course", owner=self.user)

        self.url_subscribe = reverse("users:subscription-list")  # URL для создания подписки
        self.url_unsubscribe = reverse("users:subscription-list",)

    def test_subscribe(self):
        # # Аутентификация пользователя
        # self.client.force_authenticate(user=self.user)

        # Отправляем запрос для подписки
        response = self.client.post(self.url_subscribe, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка успешного создания
        self.assertEqual(response.data["message"], "Подписка добавлена")

    def test_subscribe_duplicate(self):
        # # Аутентификация пользователя
        # self.client.force_authenticate(user=self.user)

        # Подписка на курс
        self.client.post(self.url_subscribe, {"course_id": self.course.id})

        # Пробуем подписаться повторно
        response = self.client.post(self.url_subscribe, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка успешного запроса
        self.assertEqual(response.data["message"], "Подписка уже существует")

    def test_unsubscribe(self):
        # # Аутентификация пользователя
        # self.client.force_authenticate(user=self.user)

        # Создаем подписку
        self.client.post(self.url_subscribe, {"course_id": self.course.id})

        # Формируем URL для удаления с передачей course_id
        url_with_course_id = f"{self.url_unsubscribe}{self.course.id}/"

        # Запрос на удаление подписки
        response = self.client.delete(url_with_course_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверка успешного удаления

    def test_unsubscribe_not_found(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        self.url_unsubscribe = reverse('users:subscription-detail', kwargs={'course_id': 1})

        # Попробуем удалить подписку, когда ее нет
        response = self.client.delete(self.url_unsubscribe)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Проверка на несуществующую подписку

    def test_unauthenticated_access(self):
        # Проверка доступа без аутентификации
        self.client.logout()  # Выход из системы для теста аутентификации
        response = self.client.post(self.url_subscribe, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Доступ запрещен

        # Измените url_unsubscribe, чтобы включить course_id
        response = self.client.delete(self.url_unsubscribe)  # Проверяем URL для существующей подписки
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Доступ запрещен


class PaymentTests(APITestCase):
    def setUp(self):
        # Создание пользователя и логин
        self.user = User.objects.create(
            email='test@example.com', password='testpass'  # Используйте create вместо create_user
        )
        self.user.set_password('testpass')  # Устанавливаем пароль
        self.user.save()  # Сохраняем пользователя

        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Создаем тестовые объекты курса и урока
        self.course = Course.objects.create(name="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(title="Тестовый урок", owner=self.user)
        # Создаем платёж
        self.payment = Payment.objects.create(
            user=self.user, course=self.course, lesson=self.lesson, amount=100.00, payment_method="cash"
        )

    def test_create_payment(self):
        # URL для создания платежа
        url = reverse("users:payments_create")
        data = {
            "user": self.user.id,
            "course": self.course.id,
            "lesson": self.lesson.id,
            "amount": 150.00,
            "payment_method": "transfer",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем, что создание прошло успешно

    def test_list_payments(self):
        url = reverse("payment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что список доступен

    def test_update_payment(self):
        url = reverse("users:payments_update", args=[self.payment.id])
        data = {
            "amount": 200.00,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что обновление прошло успешно

    def test_delete_payment(self):
        url = reverse("users:payments_delete", args=[self.payment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверяем, что удаление прошло успешно
