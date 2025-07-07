from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    # Добавляем поле password, чтобы оно стало доступным при создании пользователя
    password = serializers.CharField(write_only=True)  # Доступно только для записи

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_active', 'password')

    def create(self, validated_data):
        # Удаляем пароль из данных для создания пользователя
        password = validated_data.pop('password')  # Извлекаем пароль
        user = User(**validated_data)  # Создаем объект пользователя без пароля
        user.set_password(password)  # Устанавливаем пароль здесь
        user.save()  # Сохраняем пользователя
        return user
