from rest_framework.permissions import BasePermission
from parkinglot.models import UserTypeChoices

class VehiclePermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == "GET":
            return user.is_authenticated and user.user_type == UserTypeChoices.CUSTOMER
        if request.method == "POST":
            return True