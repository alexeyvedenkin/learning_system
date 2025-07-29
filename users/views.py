from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework.filters import OrderingFilter

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


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


class SubscriptionView(APIView):
    def post(self, request):
        # Логика для добавления подписки
        # Получение данных из запроса (например, user_id и course_id)
        # Создание записи в Subscription
        return JsonResponse({'status': 'подписка добавлена'})


    def delete(self, request):
        # Логика для удаления подписки
        # Получение данных и удаление записи из Subscription
        return JsonResponse({'status': 'подписка удалена'})

