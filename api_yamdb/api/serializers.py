from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from reviews.models import Comment, Category, Genre, GenreTitle, Title, Review
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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadOnlySerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'


class GenreTitleSerializer(serializers.Serializer):

    class Meta:
        model = GenreTitle
        fields = '__all_'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        # unique=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            review = Review.objects.filter(
                title=title,
                author=author,
            )
            if review.exists():
                raise 'Вы уже оставляли отзыв.'
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        # unique=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
