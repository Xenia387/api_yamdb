from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """Разрешение для админа или суперюзера."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Изменять записи может только их автор."""
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )


class IsAdminOrOther(permissions.BasePermission):
    """Разрешение для админа или суперюзера."""
    def has_permission(self, request, view):
        """Создавать, изменять и удалять категории, жанры и произведения
        может только админ."""
        return (
            (
                request.user.is_authenticated
                and request.user.is_admin
            )
            or request.method in permissions.SAFE_METHODS
        )
