from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, Review, Title
from users.models import User
from reviews.filter import TitleFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsSelfOrAdmin,
                             ReadOnlyForUnauthorized)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer,
                             TitleReadSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from api.mixins import CustomGenreCategoryViewSet, CustomTitleViewSet


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление модели отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (ReadOnlyForUnauthorized,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = self.kwargs.get('title_id')
        return context

    def title_object(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.title_object()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.title_object()
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentsViewSet(viewsets.ModelViewSet):
    """Представление модели комментов."""
    serializer_class = CommentSerializer
    permission_classes = (ReadOnlyForUnauthorized,)

    def review_object(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            Review,
            title=title,
            id=self.kwargs.get('review_id')
        )
        return review

    def get_queryset(self):
        review = self.review_object()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.review_object()
        serializer.save(
            author=self.request.user,
            review=review
        )


class UserViewSet(viewsets.ModelViewSet):
    """Представление модели пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(methods=['get', 'patch'],
            detail=False,
            url_name='me',
            url_path='me',
            permission_classes=(IsSelfOrAdmin,))
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupView(generics.GenericAPIView):
    """Представление регистрации нового пользователя."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(username=user_data['username'])
        email_body = (f'Здравствуйте {user.username}. Используйте код ниже,'
                      ' чтобы верифицировать вашу почту:\n'
                      f'{user.confirmation_code}')
        send_mail('Verify your email', email_body, 'from@example.com',
                  [user.email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(TokenObtainPairView):
    """Представление получения токена пользователем."""
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class CategoryViewSet(CustomGenreCategoryViewSet):
    """Представление модели категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class GenreViewSet(CustomGenreCategoryViewSet):
    """Представление модели жантра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class TitleViewSet(CustomTitleViewSet):
    """Представление модели произведения."""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by('name')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleSerializer
