from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginators import CustomPageNumberPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Subscription
from users.permissions import IsModer, IsOwner

from materials.tasks import send_course_update_email, send_lesson_update_email

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by("name")
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModer,)
        else:
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()  # Сохраняем курс
        # Получаем пользователей, подписанных на данный курс
        subscribers = Subscription.objects.filter(course=course).values_list('user__email', flat=True)
        # Вызываем асинхронную задачу для отправки письма
        send_course_update_email.delay(list(subscribers), course.name)  # Асинхронный вызов задачи


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all().order_by("title")
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all().order_by("title")
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all().order_by("title")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all().order_by("title")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def perform_update(self, serializer):
        lesson = serializer.save()  # Сохраняем урок
        # Получаем пользователей, подписанных на данный урок
        subscribers = Subscription.objects.filter(lesson=lesson).values_list('user__email', flat=True)
        # Вызываем асинхронную задачу для отправки письма
        send_course_update_email.delay(list(subscribers), lesson.title)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all().order_by("title")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
