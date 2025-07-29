from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginators import CustomPageNumberPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
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


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
