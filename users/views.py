from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payment, Subscription, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Закрываем доступ ко всем методам для неавторизованных пользователей

    def get_permissions(self):
        # Позволяем доступ только для создания и получения (CRUD) неавторизованным пользователям
        if self.action in ['create', 'list']:
            return [AllowAny()]  # Открываем доступ для регистрации и списка пользователей
        return super().get_permissions()  # Для остальных методов - доступ только для авторизованных

    def get_queryset(self):
        return super().get_queryset().prefetch_related('payments')

    def retrieve(self, request, *args, **kwargs):
        """ Переопределяем метод retrieve для проверки доступа """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)  # Используем сериализатор для возврата данных


class PaymentCreateApiView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method", "user",)
    ordering_fields = ("payment_date",)
    ordering = ("payment_date",)

    def list(self, request, *args, **kwargs):
        # Выводим запрашиваемый порядок сортировки
        print(f"Запрашиваемый порядок сортировки: {request.query_params.get('ordering')}")
        return super().list(request, *args, **kwargs)

class PaymentRetrieveApiView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyApiView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item, created = Subscription.objects.get_or_create(user=user, course=course_item)
        message = 'Подписка добавлена' if created else 'Подписка уже существует'
        return Response({"message": message}, status=status.HTTP_200_OK)

    def delete(self, request, course_id):
        user = request.user
        course_item = get_object_or_404(Course, id=course_id)

        # Удаляем подписку
        deleted_count = Subscription.objects.filter(user=user, course=course_item).delete()
        if deleted_count[0] > 0:
            return Response({"message": "Подписка удалена"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Подписка не найдена"}, status=status.HTTP_404_NOT_FOUND)
