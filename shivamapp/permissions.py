from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsSuperuserOrAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.author == request.user
    

class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the required role
        return request.user and request.user.role == "authorized"
