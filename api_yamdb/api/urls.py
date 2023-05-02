from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewset,
    # CommentViewSet,
    GenreViewset,
    TitleViewset,
    # ReviewViewset,
    UserSignupViewSet,
    UserReceiveTokenViewSet,
    UserViewSet,
)

v1 = DefaultRouter()
v1.register('categories', CategoryViewset, basename='categories')
v1.register('genres', GenreViewset, basename='genres')
v1.register('titles', TitleViewset, basename='titles')
v1.register('users', UserViewSet, basename='users')
# v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewset,
#     basename='reviews'
# )
# v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )

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
