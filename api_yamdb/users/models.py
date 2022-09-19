from django.contrib.auth.models import AbstractUser
from django.db import models

SAFE_ROLE = ['admin', 'moderator']


class User(AbstractUser):
    """Переопределение модели пользователя."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ACCESS_ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]

    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    role = models.CharField(
        'Роль',
        max_length=150,
        choices=ACCESS_ROLE,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    confirmation_code = models.CharField(
        'Код поддтверждения',
        max_length=150,
        blank=True
    )

    username = models.CharField(db_index=True,
                                max_length=150,
                                unique=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def is_moderator(self):
        return self.role == 'moderator'

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'
