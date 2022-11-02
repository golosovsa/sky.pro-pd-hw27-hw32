from rest_framework import permissions


class AdOwnerPermissions(permissions.DjangoModelPermissions):
    message = "Only for owners"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
