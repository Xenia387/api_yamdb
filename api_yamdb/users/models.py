from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import EMAIL_MAX_LENGTH

USER_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Email адрес',
        max_length=EMAIL_MAX_LENGTH,
        blank=False,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=32,
        choices=USER_ROLES,
        default='user',
        blank=False
    )

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'
