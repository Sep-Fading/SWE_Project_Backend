from rest_framework import permissions

"""
    This file handles permissions for accessing
    different APIs.
"""

class HasAdminAccess(permissions.BasePermission):
    # Allows Admin Access Only!

    # Checks for Admin permission and returns
    # a boolean.
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_permission == 'ADMIN'
