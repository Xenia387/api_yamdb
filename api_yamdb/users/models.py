from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRoles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        verbose_name='Email адрес',
        max_length=254,
        blank=False,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=16,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        blank=False
    )

    class Meta:
        ordering = ('username',)
