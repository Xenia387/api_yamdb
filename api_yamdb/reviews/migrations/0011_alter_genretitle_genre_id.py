# Generated by Django 3.2 on 2023-04-28 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_alter_title_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genretitle',
            name='genre_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre', verbose_name='Жанр(ы)'),
        ),
    ]
