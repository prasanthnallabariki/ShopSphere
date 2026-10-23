from rest_framework.permissions import BasePermission
from .models import User

class IsCustomer(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == User.Role.CUSTOMER

class IsSeller(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == User.Role.SELLER

class IsAdmin(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == User.Role.ADMIN

class IsSellerOrAdmin(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in [User.Role.ADMIN, User.Role.SELLER] 
