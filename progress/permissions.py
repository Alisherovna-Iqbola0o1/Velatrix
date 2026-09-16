from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Foydalanuvchi faqat O'ZIGA tegishli progress ma'lumotini ko'ra oladi.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
