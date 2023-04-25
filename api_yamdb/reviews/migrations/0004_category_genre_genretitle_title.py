# Generated by Django 3.2 on 2023-04-25 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0003_auto_20230425_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название категории не должно быть длиннее 200 символов', max_length=200, verbose_name='Название категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Адрес категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название жанра не должно быть длиннее 200 символов', max_length=200, verbose_name='Название жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Адрес жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения не должно быть длиннее 500 символов', max_length=500, verbose_name='Название произведения')),
                ('year', models.DateTimeField(verbose_name='Дата выпуска')),
            ],
            options={
                'verbose_name': 'Произведение',
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genre', to='reviews.genre', unique=True, verbose_name='Жанр(ы)')),
                ('title_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='title', to='reviews.title', unique=True)),
            ],
        ),
    ]
