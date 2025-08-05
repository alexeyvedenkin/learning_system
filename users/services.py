import stripe

from config import settings
from materials.models import Course, Lesson
from .models import Payment, User



stripe.api_key = settings.STRIPE_API_KEY


def create_payment_session(course_or_lesson):
    # Создаем продукт в Stripe
    product = stripe.Product.create(
        name=course_or_lesson.title,  # Используем название курса или урока
    )

    # Создаем цену
    price = stripe.Price.create(
        unit_amount=int(course_or_lesson.get_price() * 100),  # Цена в центах
        currency="usd",  # Валюта
        product=product.id,
    )

    # Создаем сессию
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )

    # Сохраняем платеж в модели Payment
    payment = Payment.objects.create(
        user=User,  # Укажите пользователя
        course=course_or_lesson if isinstance(course_or_lesson, Course) else None,
        lesson=course_or_lesson if isinstance(course_or_lesson, Lesson) else None,
        amount=course_or_lesson.get_price(),
        payment_method="transfer",  # Укажите способ оплаты, если нужно
    )

    return {
        "id": checkout_session.id,
        "url": checkout_session.url,
    }