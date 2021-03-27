from rest_framework import serializers
from parkinglot.models import User
from customer.models import Customer
from parkinglot.serializers import UserListSerializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ()


class CustomerListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Customer
        exclude = ()