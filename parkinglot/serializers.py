from rest_framework import serializers
from .models import Parking, ParkingLot, Transaction, User, Charges

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
        charges = Charges.objects.filter(parking_lot_ref=data.user.id)
        serializer = ChargesSerializer(charges, many=True)
        return serializer.data
    class Meta:
        model = ParkingLot
        exclude = ()

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        exclude = ()

class ParkingListSerializer(serializers.ModelSerializer):
    transaction = serializers.SerializerMethodField("fetch_transaction")
    def fetch_transaction(self, data):
        try:
            transaction = Transaction.objects.get(parking_ref=data.id)
            serializer = TransactionSerializer(transaction)
            return serializer.data
        except Transaction.DoesNotExist:
            return False
    parking_lot_ref = ParkingLotListSerializer(read_only=True)
    class Meta:
        model = Parking
        exclude = ()

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        excude = ()
