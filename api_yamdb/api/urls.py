from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewViewSet, SignupView, TitleViewSet, TokenAPIView,
                       UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_auth_urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenAPIView.as_view(), name='token'),
]

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='user')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_auth_urlpatterns)),
]
