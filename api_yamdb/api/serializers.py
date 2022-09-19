import json

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text',
            'author', 'score',
            'pub_date',
        )

    def validate(self, data):
        author = self.context.get('request').user
        title = self.context.get('title')
        review = Review.objects.filter(title=title, author=author)
        if review.exists() and self.context.get('request').method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли рецензию на это произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text',
            'author', 'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )

    def validate_username(self, username):
        if 'me' == username.lower():
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено!'
            )
        return username

    def validate(self, attrs):
        user = self.context['request'].user
        if 'role' in attrs and user.is_user():
            attrs.pop('role')
        return attrs


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if 'me' == username.lower():
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено!'
            )
        return username

    def validate_password(self, password):
        return make_password(password)

    def create(self, validated_data):
        confirmation_code = BaseUserManager().make_random_password()
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            confirmation_code=confirmation_code,
            is_active=True
        )
        user.save()
        return user


class TokenSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена."""
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.pop('confirmation_code')
        user = get_object_or_404(User, username=username)
        attrs.update({'password': ''})
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код')
        attrs = json.loads(json.dumps(attrs))
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        authenticate_kwargs["request"] = self.context.get('request')
        self.user = User.objects.get(username=authenticate_kwargs['username'])
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        refresh = self.get_token(self.user)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return {'token': str(refresh.access_token)}
