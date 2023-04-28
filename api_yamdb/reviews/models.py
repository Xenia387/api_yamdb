from django.db import models


class Category(models.Model):
    name = models.CharField(
        help_text='Название категории не должно быть длиннее 50 символов',
        max_length=50,
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
        # max_length=50,
        unique=True,
        verbose_name='Адрес жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        help_text='Название произведения не должно быть длиннее 256 символов',
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.DateTimeField(
        verbose_name='Дата выпуска'
    )
    category = models.OneToOneField(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_title',
        verbose_name='Категория произведения'
    ),

    class Meta:
        verbose_name = 'Произведение'


class GenreTitle(models.Model):
    title_id = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre_id = models.OneToOneField(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр(ы)',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='genreoftitle'
            )
        ]
