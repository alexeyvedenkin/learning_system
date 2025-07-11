from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserManager(BaseUserManager):
    """
    Кастомный менеджер моделей, в котором электронная почта является уникальным идентификатором
    для аутентификации вместо имени пользователя.
    """

    def __init__(self, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model  # Сохраняем модель пользователя

    def create_user(self, email, password, first_name=None, last_name=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError(_("Необходимо указать e-mail"))

        # Нормализуем адрес электронной почты
        email = self.normalize_email(email)

        # Создаем username как комбинацию first_name и last_name
        username = (first_name + last_name).replace(" ", "")  # Убираем пробелы

        # Создаем нового пользователя без передачи username
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)

        # Устанавливаем пароль
        user.set_password(password)
        user.save()
        return user
