from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import (
    IsAdminOrSuperUser,
    IsAuthorOrAdminOrReadOnly,
    IsAdminOrOther
)
from .utils import send_confirmation_code
from .serializers import (
    CategorySerializer,
    # CommentSerializer,
    GenreSerializer,
    TitleSerializer,
    # ReviewSerializer,
    UserSignupSerializer,
    UserRecieveTokenSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Title
from users.models import User


class UserSignupViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Создание пользователя и отправка кода
    подтверждения на его email.
    """
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        send_confirmation_code(
            email=user.email,
            confirmation_code=default_token_generator.make_token(user)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReceiveTokenViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Выдача JWT токена."""
    queryset = User.objects.all()
    serializer_class = UserRecieveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Код подтверждения не подходит.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        detail=False,
        methods=['get', 'post', 'patch'],
        permission_classes=[
            permissions.IsAuthenticated
        ],
        url_path='me',
    )
    def himself(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """"Создание и удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrOther,)
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class GenreViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Создание и удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrOther,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class TitleViewset(viewsets.ModelViewSet):
    """Создание, частичное обновление и удаление произведений."""
    queryset = Title.objects.all()
    # queryset = Title.objects.all().annotate(
    #     rating=Avg('reviews__score')
    # ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrOther,)
    pagination_class = None
    filter_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    # def create(self, request):
    #     serializer = TitleSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(
    #             serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #         )
    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, pk):
        Title.objects.filter(pk=self.kwargs.get(id)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None):
        title = Title.objects.filter(pk=self.kwargs.get(id))
        title.update()
        return Response(title, status=status.HTTP_201_CREATED)


# class ReviewViewset(viewsets.ModelViewSet):
#     """"Работа с отзывами.
#         Получить, добавить,
#         отредактировать, удалить отзыв.
#     """
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = (IsAuthorOrAdminOrReadOnly,)

#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()

#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         serializer.save(author=self.request.user, title=title)


# class CommentViewSet(viewsets.ModelViewSet):
#     """"Работа с отзывами к комментариям.
#         Получить, добавить,
#         отредактировать, удалить
#         комментарий к отзыву.
#     """
#     # queryset = Review.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (IsAuthorOrAdminOrReadOnly,)

#     def get_queryset(self):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         return review.comments.all()

#     def perform_create(self, serializer):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         serializer.save(author=self.request.user, review=review)
