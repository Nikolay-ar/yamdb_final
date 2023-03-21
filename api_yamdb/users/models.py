from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import username_validator

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = (
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь'),
)


class User(AbstractUser):
    """Создание кастомного класса User, описание базовых функций"""

    username = models.CharField(
        max_length=settings.FIELD_MAX_LENGTH,
        unique=True,
        db_index=True,
        validators=[username_validator],
        verbose_name='Никнейм'
    )

    email = models.EmailField(
        max_length=settings.FIELD_EMAIL_LENGTH,
        unique=True,
        verbose_name='Почта'
    )

    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография/О пользователе',
        help_text='Расскажите о себе'
    )

    role = models.CharField(
        max_length=max([len(role) for role, name in ROLES]),
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя'
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    def __str__(self):
        return self.username
