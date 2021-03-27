from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from parkinglot.models import User
from customer.serializers import CustomerSerializer
from rest_framework import status
from customer.models import Customer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.

class LoginCustomer(APIView):
    def post(self, request):
        print(request.data)
        username = request.data['mobile']
        password = request.data['password']``
        try:

            customer = User.objects.get(mobile=username)
            print(customer.password)
            if customer.password == password:
                try:
                        
                    serializerData = CustomerSerializer(data=request.data, format=None)
                    if serializerData.is_valid():
                        print(serializerData.data)
                        return Response(data=serializerData.data, status=status.HTTP_200_OK,)
                    
                except Exception as e:
                    print(e)
                    return Response(data=serializerData.errors, status=status.HTTP_400_BAD_REQUEST,)
                
            else:
                print("Asdkjjba")
                return Response(data=None)
        except Exception as e:
            print(e)
            return Response(data=None,  status=status.HTTP_400_BAD_REQUEST)

class CustomerById(APIView):
    def get(self, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            return Response(
                data=customer
             , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                data=None,
                status=status.HTTP_400_BAD_REQUEST
            )   

class InsertCustomer(APIView):
    def post(self, request, format='json'):
        req_data = request.data
        print(req_data)
        try:
            customer = User.objects.get(mobile=req_data['mobile'])
            return Response(data=None)
        except User.DoesNotExist:
            password = req_data['password']
            customer = User.objects.create(req_data)
            customer.save()
        
        serializer = CustomerSerializer(data=req_data, format=None)
        if serializeer.is_valid():
            serializer.save()
            return Response(
                    data=serializer.data,
                     
                    status=status.HTTP_200_OK
                )
        else:
             return Response(
                    data=serializer.errors,
                    
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

