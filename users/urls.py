from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (PaymentCreateApiView, PaymentDestroyApiView, PaymentListApiView, PaymentRetrieveApiView,
                         PaymentUpdateApiView, SubscriptionAPIView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    path('payments/', PaymentListApiView.as_view(), name='payments_list'),
    path('payments/create/', PaymentCreateApiView.as_view(), name='payments_create'),
    path('payments/<int:pk>/', PaymentRetrieveApiView.as_view(), name='payments_retrieve'),
    path('payments/<int:pk>/update/', PaymentUpdateApiView.as_view(), name='payments_update'),
    path('payments/<int:pk>/delete/', PaymentDestroyApiView.as_view(), name='payments_delete'),

    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription-list'),  # для создания и получения подписок
    path('subscriptions/<int:course_id>/', SubscriptionAPIView.as_view(), name='subscription-detail'),  # для удаления подписки
]

urlpatterns += router.urls
