from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):

    # Добавляем новое поле для количества уроков
    lesson_count = SerializerMethodField()  # Создаем поле для вычисляемого значения

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        """ Метод для получения количества уроков """
        return obj.lesson_set.count()  # Используем обратное отношение для доступа к урокам и считаем их


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
