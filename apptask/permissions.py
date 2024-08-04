from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'ADMIN'

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'MANAGER'

class IsUserUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'USER'


class IsAdminOrManagerUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        print(f"User: {user}")
        print(f"User's user_type: {user.user_type}")
        return request.user and (
            request.user.user_type == 'ADMIN' or
            request.user.user_type == 'MANAGER'
        )
class IsAdminOrManagerOrUserUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.user_type == 'ADMIN' or
            request.user.user_type == 'MANAGER' or
            request.user.user_type == 'USER'
        )
