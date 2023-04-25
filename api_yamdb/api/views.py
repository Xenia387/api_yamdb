from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .serializers import (
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
    permission_classes = (permissions.AllowAny,)
