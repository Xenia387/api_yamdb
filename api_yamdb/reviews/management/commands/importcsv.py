import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Comment, Category, Genre, Title, GenreTitle, Review
from users.models import User

CSV_DATA = {
    Category: ('category.csv', ('id', 'name', 'slug')),
    Genre: ('genre.csv', ('id', 'name', 'slug')),
    Title: ('titles.csv', ('id', 'name', 'year', 'category_id')),
    GenreTitle: ('genre_title.csv', ('id', 'title_id', 'genre_id')),
    User: (
        'users.csv',
        ('id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name')
    ),
    Review: (
        'review.csv', ('id', 'title_id', 'text', 'author', 'score', 'pub_date')
    ),
    Comment: (
        'comments.csv', ('id', 'review_id', 'text', 'author', 'pub_date')
    ),
}

CSV_PATH = f'{settings.BASE_DIR}/statis/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        records = []
        for model, csv_file in CSV_DATA.items():
            with open(str(CSV_PATH) + csv_file[0], 'r',) as file:
                reader = csv.DictReader(
                    file, delimiter=',',
                    fieldsname=csv_file[1],
                )
                for row in reader:
                    record = model(**row)
                    records.append(record)
            model.objects.bulk_create(records)
            self.stdout.write(self.style.SUCCESS('Данные импортированы'))
