from typing import Tuple

from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Класс для админки ролей пользователей."""
    list_display: Tuple[str, ...] = ('pk', 'username', 'email',
                                     'first_name', 'last_name',
                                     'role',)
    list_editable: Tuple[str, ...] = ('role',)
    search_fields: Tuple[str, ...] = ('role', 'username')
    list_filter: Tuple[str, ...] = ('role',)
    empty_value_display: str = '-пусто-'


admin.site.register(User, UserAdmin)
