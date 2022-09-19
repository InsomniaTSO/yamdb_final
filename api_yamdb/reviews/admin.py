from django.contrib import admin
from reviews.models import Category, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    """Класс для админки произведений."""
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    """Класс для админки жанров."""
    list_display = ('name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    """Класс для админки категорий."""
    list_display = ('name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Класс для админки отзывов."""
    list_display = ('title', 'score')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
