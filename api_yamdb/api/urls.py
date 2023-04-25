from django.urls import path

from .views import (
    UserSignupViewSet,
    UserReceiveTokenViewSet,
)


urlpatterns = [
    path(
        'v1/auth/signup/',
        UserSignupViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        UserReceiveTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
]
