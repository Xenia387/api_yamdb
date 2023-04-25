from django.urls import path

from users.views import (
    UserCreateViewSet,
    UserReceiveTokenViewSet,
)


urlpatterns = [
    path(
        'v1/auth/signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        UserReceiveTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
]
