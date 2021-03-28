from rest_framework import serializers
from .models import Parking, ParkingLot, User, Charges

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "mobile") 

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        exclude = ()


class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        exclude = ()


class ParkingLotListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    charges = serializers.SerializerMethodField("fetch_charges")
    def fetch_charges(self, data):
        print(data.user.id)
        charges = Charges.objects.filter(parking_lot_ref=data.user.id)
        serializer = ChargesSerializer(charges, many=True)
        return serializer.data
    class Meta:
        model = ParkingLot
        exclude = ()

class ParkingSerializer(serializers.ModelSerializer):
    parking_lot_ref = ParkingLotListSerializer(read_only=True)
    class Meta:
        model = Parking
        exclude = ()
