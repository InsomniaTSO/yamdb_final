import datetime

from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User

now = datetime.datetime.now()

TEXT_COMMENT = 10
TEXT_TITLE = 10
TEXT_REVIEW = 15

SCORE_CHOICES = (
    (1, 1), (2, 2),
    (3, 3), (4, 4),
    (5, 5), (6, 6),
    (7, 7), (8, 8),
    (9, 9), (10, 10)
)


class Category(models.Model):
    """Модель категории."""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг названия', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField('Название жанра', max_length=50)
    slug = models.SlugField('Слаг названия', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField('Название произведения', max_length=100)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(now.year)])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:TEXT_TITLE]


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст отзыва',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:TEXT_REVIEW]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Модель комментария."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField('Текст комментария',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_COMMENT]
