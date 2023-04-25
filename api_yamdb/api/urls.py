from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserSignupViewSet,
    UserReceiveTokenViewSet,
    UserViewSet,
)

v1 = DefaultRouter()
v1.register('users', UserViewSet, basename='users')

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
    path('v1/', include(v1.urls)),
]
