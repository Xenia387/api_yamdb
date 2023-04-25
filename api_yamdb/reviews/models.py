from django.db import models


class Category(models.Model):
    category = models.CharField(
        help_text='Название категории не должно быть длиннее 200 символов',
        max_length=200,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    genre = models.CharField(
        help_text='Название жанра не должно быть длиннее 200 символов',
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    title = models.CharField(
        help_text='Название произведения не должно быть длиннее 500 символов',
        max_length=500,
        verbose_name='Название произведения'
    )
    author = models.CharField(
        help_text='Название категории не должно быть длиннее 200 символов',
        max_length=200,
        verbose_name='Автор произведения'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата выпуска'
    )
    description = models.TextField(
        help_text='Добавьте описание произведения',
        verbose_name='Описание произведния'
    )
    category = models.OneToOneField(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения'
    ),
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр(ы) произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
