import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter()
    year = django_filters.DateTimeFilter()
    category__slug = django_filters.CharFilter()
    genre__slug = django_filters.CharFilter()

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
