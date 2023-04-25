from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title
from users.models import User


class UserSignupSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=r'' + UnicodeUsernameValidator.regex,
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username "me".'
            )
        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            user = User.objects.get(email=data['email'])
            if user.username != data['username']:
                raise serializers.ValidationError(
                    'Для этого email уже существует другой пользователь'
                )
        if User.objects.filter(username=data['username']).exists():
            user = User.objects.get(username=data['username'])
            if user.email != data['email']:
                raise serializers.ValidationError(
                    'Для этого пользователя указан другой email'
                )
        return data


class UserRecieveTokenSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=r'' + UnicodeUsernameValidator.regex,
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CategorySerializer(serializers.Serializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )
        read_only_fields = (
            'id',
            'name',
            'slug',
        )


class GenreSerializer(serializers.Serializer):

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )
        read_only_fields = (
            'id',
            'name',
            'slug',
        )


class TitleSerializer(serializers.Serializer):

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category'
        )
        read_only_fields = (
            'id',
            'name',
            'year',
            'category',
        )


class GenreTitleSerializer(serializers.Serializer):

    class Meta:
        model = GenreTitle
        fields = (
            'title_id',
            'genre_id'
        )
        read_only_fields = (
            'title_id',
            'genre_id'
        )
