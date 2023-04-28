from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAdminOrSuperUser, IsAuthorOrAdminOrReadOnly
from reviews.models import Category, Genre, Title
from users.models import User
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSignupSerializer,
    UserRecieveTokenSerializer,
    UserSerializer,
)
from .utils import send_confirmation_code


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


class CategoryViewset(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """"Создание и удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
            # return Response(status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid(raise_exception=True):
            category, created = Category.objects.get_or_create(**serializer.validated_data)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        category = Category.objects.filter(pk=self.kwargs.get(id))
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewset(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Создание и удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthorOrAdminOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def create(self, request):
        if request.method == 'POST':
            serializer = GenreSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                # return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        genre = Genre.objects.filter(pk=self.kwargs.get(id))
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewset(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Создание и удаление произведенийю."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('name', 'year',)
    # фильтрация по названию году жанру и категориям slug

    def create(self, request):
        if request.method == 'POST':
            serializer = TitleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # изменяется значения полей name category
        pass

    def destroy(self, request, pk):
        title = Title.objects.filter(pk=self.kwargs.get(id))
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # проверить что запрос удалил объект из БД
