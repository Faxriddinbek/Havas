from rest_framework.permissions import BasePermission
from  rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    """Admin'lar CRUD, boshqalar faqat o'qiy oladi"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class CanSubmitSurvey(BasePermission):
    """Faqat login qilgan foydalanuvchilar so'rovnomani to'dira oladi"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
