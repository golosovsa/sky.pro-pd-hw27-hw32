from rest_framework import permissions

from users.models import User


class UserModeratorPermissions(permissions.BasePermission):
    message = "Only for moderators"

    def has_permission(self, request, view):
        if request.user.role == User.MODERATOR:
            return True
        return False


class UserAdminPermissions(permissions.BasePermission):
    message = "Only for admins"

    def has_permission(self, request, view):
        if request.user.role == User.ADMIN:
            return True
        return False


class UserOwnerPermissions(permissions.DjangoModelPermissions):
    message = "Only for owners"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class UserModeratorAndAdminCanWriteOrReadOnly(permissions.BasePermission):
    message = "Only for moderators or admins"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in [User.MODERATOR, User.ADMIN]
