# Generated by Django 3.2 on 2023-05-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_auto_20230430_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(null=True, related_name='genre_title', to='reviews.Genre', verbose_name='Жанр(ы) произведения'),
        ),
    ]
