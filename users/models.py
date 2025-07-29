from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import JsonResponse
from django.views import View


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=25, verbose_name='Имя', blank=True, null=True)
    last_name = models.CharField(max_length=25, verbose_name='Фамилия', blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=25, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='Аватар', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Payment(models.Model):
    # Связь с пользователем
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payments')
    # Дата оплаты
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    # Связь с курсом
    course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, verbose_name='Оплаченный курс')
    # Связь с уроком
    lesson = models.ForeignKey('materials.Lesson', on_delete=models.CASCADE, verbose_name='Оплаченный урок')
    # Сумма оплаты
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    # Способ оплаты: наличные или перевод
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
