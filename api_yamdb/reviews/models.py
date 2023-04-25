from django.db import models


class Category(models.Model):
    name = models.CharField(
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
    name = models.CharField(
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
    name = models.CharField(
        help_text='Название произведения не должно быть длиннее 500 символов',
        max_length=500,
        verbose_name='Название произведения'
    )
    year = models.DateTimeField(
        verbose_name='Дата выпуска'
    )
    category = models.OneToOneField(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория произведения'
    ),

    class Meta:
        verbose_name = 'Произведение'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        unique=True,
        related_name='title',
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        unique=True,
        verbose_name='Жанр(ы)',
        related_name='genre',
    )
