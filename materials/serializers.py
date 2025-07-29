import re

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import Subscription
from .validators import validate_youtube_link  # Импортируем валидатор


# Регулярное выражение для проверки ссылок на YouTube
YOUTUBE_URL_PATTERN = r'https?://(www\.)?(youtube\.com|youtu\.be)/'


class LessonSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    video_url = serializers.URLField(validators=[validate_youtube_link], required=False)  # Обозначаем, что это поле необязательное

    class Meta:
        fields = ['title', 'content', 'video_url']

    def validate(self, attrs):
        # Проверяем все ссылки в title и content
        self.validate_youtube_links_in_text(attrs.get('title'))
        self.validate_youtube_links_in_text(attrs.get('content'))
        return attrs

    def validate_youtube_links_in_text(self, text):
        """ Проверка на наличие YouTube ссылок в тексте. """
        if text:  # Проверяем, если текст присутствует
            links = re.findall(YOUTUBE_URL_PATTERN, text)  # Находим все ссылки
            for link in links:  # Проходим по каждой ссылке
                validate_youtube_link(link[0])  # Вызов валидатора для каждой ссылки


class CourseSerializer(ModelSerializer):
    # Добавляем новое поле для количества уроков
    lesson_count = SerializerMethodField()
    # Добавляем список уроков
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_subscribed']

    def get_lesson_count(self, obj):
        """ Метод для получения количества уроков """
        return obj.lessons.count()  # Используем обратное отношение для доступа к урокам и считаем их

    def validate(self, attrs):
        for lesson in attrs.get('lessons', []):
            video_url = lesson.get('video_url')
            if video_url:  # Проверка для видео-ссылки
                validate_youtube_link(video_url)
        # Проверяем все ссылки в name и description курса
        self.validate_youtube_links_in_text(attrs.get('name'))
        self.validate_youtube_links_in_text(attrs.get('description'))
        return attrs

    def validate_youtube_links_in_text(self, text):
        """ Проверка на наличие YouTube ссылок в тексте. """
        if text:
            links = re.findall(YOUTUBE_URL_PATTERN, text)  # Найти все YouTube ссылки
            for link in links:  # Проходим по каждой ссылке
                validate_youtube_link(link[0])  # Вызов валидатора для каждой ссылки

    def get_is_subscribed(self, obj):
        user = self.context['request'].user  # Получаем текущего пользователя
        return Subscription.objects.filter(user=user, course=obj).exists()  # Проверяем, есть ли подписка
