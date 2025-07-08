from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


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
