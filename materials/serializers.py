from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from .validators import validate_youtube_link  # Импортируем наш валидатор


class LessonSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    video_url = serializers.URLField(validators=[validate_youtube_link])  # Используем функцию-валидатор

    class Meta:
        fields = ['title', 'content', 'video_url']


class CourseSerializer(ModelSerializer):

    # Добавляем новое поле для количества уроков
    lesson_count = SerializerMethodField()
    # Добавляем список уроков
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        """ Метод для получения количества уроков """
        return obj.lessons.count()  # Используем обратное отношение для доступа к урокам и считаем их

    class CourseSerializer(ModelSerializer):
        # Добавляем новое поле для количества уроков
        lesson_count = SerializerMethodField()
        # Добавляем список уроков
        lessons = LessonSerializer(many=True, read_only=True)

        class Meta:
            model = Course
            fields = '__all__'

        def get_lesson_count(self, obj):
            """ Метод для получения количества уроков """
            return obj.lessons.count()  # Используем обратное отношение для доступа к урокам и считаем их
