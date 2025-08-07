import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


# Функция для создания продукта
def create_product(product_type):
    """Функция для создания продукта"""
    # Создаем продукт в Stripe и возвращаем его название
    product = stripe.Product.create(name=product_type)
    return product.id


def create_stripe_price(product_id, amount):
    """Функция для создания цены продукта"""

    price = stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product=product_id,
    )
    return price


def create_payment_session(price):
    """Функция для создания платежной сессии в Stripe"""
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price.get("id"),
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
    )

    return session.get("id"), session.get("url")  # Возвращаем id и url сессии
