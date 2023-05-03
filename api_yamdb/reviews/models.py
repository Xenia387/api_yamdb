from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(
        help_text='Название категории не должно быть длиннее 50 символов',
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Адрес категории'
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        help_text='Название жанра не должно быть длиннее 200 символов',
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес жанра'
    )

    class Meta:
        ordering = ['slug']
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
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_title',
        verbose_name='Категория произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )

    class Meta:
        ordering = ['year']
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Текст комментария',
    )

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_constraint'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        help_text='Комментарий не более 1000 символов',
        max_length=1000,
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('id', )
