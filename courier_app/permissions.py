from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsDeliveryMan(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'delivery'

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'
