from rest_framework.permissions import BasePermission
from parkinglot.models import Charges, UserTypeChoices

class VehiclePermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == "GET":
            return user.is_authenticated and user.user_type == UserTypeChoices.CUSTOMER
        if request.method == "POST":
            return True

class ChargesListPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == "POST":
            return user.is_authenticated and (user.user_type == UserTypeChoices.PARKING_LOT)
        elif request.method == "GET":
            return True
        else:
            return False


class ChargesDetailPermissions(BasePermission):
    def has_permission(self, request, view, **kwargs):
        user = request.user
        if request.method in ["PUT", "DELETE"] and user.is_authenticated and (user.user_type == UserTypeChoices.PARKING_LOT):
            pk = view.kwargs["pk"]
            try:
                charges = Charges.objects.get(id=pk, parking_lot_ref=user.id)
                request.charges = charges
                return True
            except Charges.DoesNotExist:
                return False

        else:
            return False