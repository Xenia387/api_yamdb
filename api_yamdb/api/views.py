from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOrSuperUser, IsAdminOrOther
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
from .filters import TitleFilter


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


class CategoryViewset(viewsets.ModelViewSet):
    """"Создание и удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrOther,)
    http_method_names = ['get', 'post', 'delete']

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        category = Category.objects.filter(pk=self.kwargs.get(id))
        category.delete()
        if not category.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewset(viewsets.ModelViewSet):
    """Создание и удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrOther,)
    # pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'delete']

    def create(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        Genre.objects.filter(pk=self.kwargs.get(id)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewset(viewsets.ModelViewSet):
    """Создание и удаление произведений."""
    queryset = Title.objects.all()
    # queryset = Title.objects.all().annotate(
    #     rating=Avg('reviews__scrore').order_by('name')
    # )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrOther,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filter_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, pk):
        Title.objects.filter(pk=self.kwargs.get(id)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None):
        title = Title.objects.filter(pk=self.kwargs.get(id))
        title.update()
        return Response(title, status=status.HTTP_201_CREATED)
