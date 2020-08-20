from rest_framework import permissions


# create IsOwner Method
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    A custom class to allow users to view only if the the user is
    owner of that object
    """
    def has_object_permission(self, request, view, obj):

        # check if the request is in safe methods

        return obj.uid == request.user.uid


class IsSuperAdminOrStaff(permissions.BasePermission):
    """
    A custom class to check if user is admin or staff
    """
    def has_permission(self, request, view):

        return request.user.is_staff or request.user.is_superuser


class IsOwnerAttributes(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.user.uid == request.user.uid
