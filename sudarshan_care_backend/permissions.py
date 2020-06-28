from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.is_owner(request.user)


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff
