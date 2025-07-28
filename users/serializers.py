from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):

    # Добавляем поле password, чтобы оно стало доступным при создании пользователя
    password = serializers.CharField(write_only=True)  # Доступно только для записи

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'city', 'is_active', 'password', 'payments')

    def create(self, validated_data):
        # Удаляем пароль из данных для создания пользователя
        password = validated_data.pop('password')  # Извлекаем пароль
        user = User(**validated_data)  # Создаем объект пользователя без пароля
        user.set_password(password)  # Устанавливаем пароль здесь
        user.save()  # Сохраняем пользователя
        return user
