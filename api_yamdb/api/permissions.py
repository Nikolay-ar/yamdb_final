from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """Проверка на администратора."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAuthorOrIsModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Кастомный класс прав на просмотр от всех пользователей"""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in 'GET'
                or request.user == obj.author
                or request.user.is_moderator or request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права только администратора, для остальных только чтение."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in SAFE_METHODS)
