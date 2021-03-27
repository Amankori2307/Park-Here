from rest_framework import views, status, viewsets
from rest_framework.response import Response
from parkinglot.models import User, UserTypeChoices
from utils.utils import check_required_fields, gen_response
from .serializers import CustomerSerializer, CustomerListSerializer, VehicleSerializer
from .models import Customer, Vehicle
from utils.permissions import VehiclePermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
# Create your views here.
class CustomerListView(views.APIView):
 
    def post(self, request):
        req_data = request.data
        errors = check_required_fields(req_data, ['mobile', 'password'])
        if len(errors.keys()):
            return Response(
                gen_response(True, False, errors),
                status=status.HTTP_400_BAD_REQUEST
            )
        mobile = req_data.get("mobile", None)
        password = req_data.get("password", None)
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(mobile=mobile, password=password, user_type=UserTypeChoices.CUSTOMER)

        req_data["user"] = user.id
        serializer = CustomerSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            token = Token.objects.get_or_create(user=user)
            token = token[0]
            data = {
                "auth_token": token.key
            }
            return Response(
                gen_response(False, True, "Successfully Added Customer", data),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                gen_response(True, False, serializer.errors)
            )

    def get(self, request):
        try:
            queryset = Customer.objects.all()
            serializer = CustomerListSerializer(queryset, many=True)
            return Response(
                gen_response(False, True, "List Of Parking Lot", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(False, True, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CustomerDetailView(views.APIView):
    def get_object(self, pk):
        try:
            obj = Customer.objects.get(pk=pk)
            return obj
        except ParkingLot.DoesNotExist:
            raise Http404
    
    def get(self, requset, pk):
        try:
            parking_lot = self.get_object(pk)
            serializer = CustomerListSerializer(parking_lot)
            return Response(
                gen_response(False, True, "", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(True, False, "Object Not Found"),
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk):
        try:
            parking_lot = self.get_object(pk)
            serializer = CustomerSerializer(parking_lot, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = CustomerListSerializer(serializer.instance).data

                return Response(
                    gen_response(False, True, "Successfully Updated Customer Lot", data),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    gen_response(True, False, serializer.errors)
                )
        except Exception as e:
            print(e)
            return Response(
                gen_response(True, False, "Object Not Found"),
                status=status.HTTP_404_NOT_FOUND
            )

class GetSelfDetails(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        user = request.user
        try: 
            parking_lot = Customer.objects.get(user=user.id)
            serializer = CustomerListSerializer(parking_lot)
            return Response(
                gen_response(False, True, "", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(True, False, "Parking Lot Not Found"),
                status=status.HTTP_404_NOT_FOUND
            )


# Vehicle Views
class VehicleListView(views.APIView):
    permission_classes = [VehiclePermissions]
    authentication_classes = [TokenAuthentication]
    def post(self, request):

        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                gen_response(False, True, "Successfully Added Vehicle"),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                gen_response(True, False, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        try:
            queryset = Vehicle.objects.all()
            serializer = VehicleSerializer(queryset, many=True)
            return Response(
                gen_response(False, True, "List Of Vehicle ", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(False, True, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CustomerDetailView(views.APIView):
    def get_object(self, pk):
        try:
            obj = Customer.objects.get(pk=pk)
            return obj
        except ParkingLot.DoesNotExist:
            raise Http404
    
    def get(self, requset, pk):
        try:
            parking_lot = self.get_object(pk)
            serializer = CustomerListSerializer(parking_lot)
            return Response(
                gen_response(False, True, "", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(True, False, "Object Not Found"),
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk):
        try:
            parking_lot = self.get_object(pk)
            serializer = CustomerSerializer(parking_lot, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = CustomerListSerializer(serializer.instance).data

                return Response(
                    gen_response(False, True, "Successfully Updated Customer Lot", data),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    gen_response(True, False, serializer.errors)
                )
        except Exception as e:
            print(e)
            return Response(
                gen_response(True, False, "Object Not Found"),
                status=status.HTTP_404_NOT_FOUND
            )
