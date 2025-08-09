from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        exclude = ["user"]

class UserSerializer(ModelSerializer):

    # Добавляем поле password, чтобы оно стало доступным при создании пользователя
    password = serializers.CharField(write_only=True)  # Доступно только для записи

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "city", "is_active", "password", "payments")

    def create(self, validated_data):
        # Удаляем пароль из данных для создания пользователя
        password = validated_data.pop("password")  # Извлекаем пароль
        user = User(**validated_data)  # Создаем объект пользователя без пароля
        user.set_password(password)  # Устанавливаем пароль здесь
        user.save()  # Сохраняем пользователя
        return user

    def to_representation(self, instance):
        """Переопределяем метод для настройки выводимых данных"""
        user_data = super().to_representation(instance)
        # Проверяем, является ли текущий пользователь владельцем профиля
        if self.context["request"].user != instance:
            # Удаляем чувствительные данные для сторонних пользователей.
            # Скрываем фамилию, если есть
            if "last_name" in user_data:
                user_data.pop("last_name")
            # Скрываем историю платежей, если есть
            if "payments" in user_data:
                user_data.pop("payments")
            # Скрываем пароль, если есть
            if "password" in user_data:
                user_data.pop("password")
        return user_data
