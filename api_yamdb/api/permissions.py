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
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
        )
# class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
#     """Изменять записи может только их автор."""
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.method == 'POST':
#             return request.user.is_authenticated
#         return (request.user.is_authenticated or (
#                 request.user == obj.author
#                 or request.user.is_moderator
#                 or request.user.is_admin
#                 or request.user.is_staff
#                 or request.user.is_superuser         
#         ))


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
