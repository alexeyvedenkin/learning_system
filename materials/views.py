from datetime import timedelta

from django.utils import timezone
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

    def update_course(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Проверяем, прошло ли более 4 часов с последнего обновления курса
        if timezone.now() - instance.last_update > timedelta(hours=4):
            subscriptions = Subscription.objects.filter(course=instance)
            for subscription in subscriptions:
                send_course_update_email.delay(subscription.user.email, instance.name)  # Отправка email

        return Response(serializer.data)


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

    def update_lesson(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all().order_by("title")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
