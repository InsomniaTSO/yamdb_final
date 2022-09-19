from rest_framework import permissions

from users.models import SAFE_ROLE


class IsAdmin(permissions.BasePermission):
    """Разрешение на редактирование только админом."""
    message = 'Доступ только у администаратора!'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin() or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin()
                or request.user.is_superuser)


class IsSelfOrAdmin(permissions.BasePermission):
    """Разрешение на редактирование только владельцем и админом."""

    message = 'Доступ только у владельца!'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj == request.user
                or request.user.is_admin())


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только админу, остальным только чтение."""
    message = 'Доступ на только у автора!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin()))


class ReadOnlyForUnauthorized(permissions.BasePermission):
    """Разрешение на отправку SAFE-методов любому пользователю."""
    message = 'Вы не авторизованы!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role in SAFE_ROLE)
