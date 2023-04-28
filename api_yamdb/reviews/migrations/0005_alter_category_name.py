# Generated by Django 3.2 on 2023-04-26 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_category_genre_genretitle_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Название категории не должно быть длиннее 50 символов', max_length=50, verbose_name='Название категории'),
        ),
    ]