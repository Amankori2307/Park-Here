from customer.models import Vehicle
from re import error, search
from utils.permissions import ChargesDetailPermissions, ChargesListPermissions
from rest_framework import request, serializers, views, status
from rest_framework.response import Response
from .models import Charges, Parking, User, UserTypeChoices
from utils.utils import check_required_fields, gen_response
from .serializers import ParkingLotSerializer, ParkingLotListSerializer, ChargesSerializer, ParkingSerializer
from .models import ParkingLot
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate

# Create your views here.
class ParkingLotListView(views.APIView):

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
            user = User.objects.create_user(mobile=mobile, password=password, user_type=UserTypeChoices.PARKING_LOT)

        req_data["user"] = user.id
        serializer = ParkingLotSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            token = Token.objects.get_or_create(user=user)
            token = token[0]
            data = {
                "auth_token": token.key
            }
            return Response(
                gen_response(False, True, "Successfully Added Parking Lot", data),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                gen_response(True, False, serializer.errors)
            )

    def get(self, request):
        try:
            queryset = ParkingLot.objects.all()
            serializer = ParkingLotListSerializer(queryset, many=True)
            return Response(
                gen_response(False, True, "List Of Parking Lot", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(False, True, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class ParkingLotDetailView(views.APIView):
    def get_object(self, pk):
        try:
            obj = ParkingLot.objects.get(pk=pk)
            print(obj)
            return obj
        except ParkingLot.DoesNotExist:
            raise Http404
    
    def get(self, requset, pk):
        try:
            parking_lot = self.get_object(pk)
            serializer = ParkingLotListSerializer(parking_lot)
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
            serializer = ParkingLotSerializer(parking_lot, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = ParkingLotListSerializer(serializer.instance).data

                return Response(
                    gen_response(False, True, "Successfully Updated Parking Lot", data),
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
            parking_lot = ParkingLot.objects.get(user=user.id)
            serializer = ParkingLotListSerializer(parking_lot)
            return Response(
                gen_response(False, True, "", serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                gen_response(True, False, "Parking Lot Not Found"),
                status=status.HTTP_404_NOT_FOUND
            )

class LoginView(views.APIView):
    def post(self, request):
        errors = check_required_fields(request.data, ["mobile", "password"])
        if len(errors.keys()):
            return Response(
                gen_response(True, False, errors),
                status=status.HTTP_400_BAD_REQUEST
            )   
        mobile = request.data["mobile"]
        password = request.data["password"]
        user = authenticate(mobile=mobile, password=password)
        print(user, mobile, password)
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            token = token[0]
            data = {
                "auth_token": token.key            }
            return Response(
                gen_response(False, True, "", data),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                gen_response(True, False, "Please Signup or Enter Valid Credentials"),
                status=status.HTTP_400_BAD_REQUEST
            )            

class ChargesListView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ChargesListPermissions]
    def post(self, request):
        req_data = request.data
        req_data["parking_lot_ref"] = request.user.id
        serializer = ChargesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                gen_response(False, True, "", serializer.data),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                gen_response(True, False, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.user_type == UserTypeChoices.PARKING_LOT:
            parking_lot_ref = request.user.id
        else:
            parking_lot_ref = request.query_params.get("parking_lot_ref", None)
            if not parking_lot_ref:
                return Response(
                    gen_response(True, False, "'parking_lot_ref' Is Required(In Query Params) "),
                    status=status.HTTP_400_BAD_REQUEST
                )
        charges_list = Charges.objects.filter(parking_lot_ref=parking_lot_ref)
        serializer = ChargesSerializer(charges_list, many=True)
        return Response(
            gen_response(False, True, "List of Charges", serializer.data),
            status=status.HTTP_200_OK
        )

class ChargesDetailView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ChargesDetailPermissions]
    def put(self, request, pk):
        charges = request.charges
        serializer = ChargesSerializer(charges, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                gen_response(False, True, "", serializer.data),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                gen_response(True, False, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self, request, pk):
        charges= request.charges
        charges.delete()
        return Response(
            gen_response(True, False, "Deleted Successfully"),
            status=status.HTTP_200_OK
        )


class ParkingListView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    def post(self, request):
        try:
            errors = check_required_fields(request.data, ["vehicle_ref", "parking_lot_ref"])
            if len(errors.keys()):
                return Response(
                    gen_response(True, False, errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Check if there is already an active parking for given vehicle in given parking
            try: 
                vehicle_ref = request.data.get("vehicle_ref", None)
                parking_lot_ref = request.data.get("parking_lot_ref", None)
                parking = Parking.objects.filter(vehicle_ref=vehicle_ref, parking_lot_ref=parking_lot_ref, payment_status=False)
                serializer = ParkingSerializer(parking, many=True)
                return Response(
                    gen_response(True, False, "1", serializer.data),
                    status=status.HTTP_200_OK
                )
            except Vehicle.DoesNotExist:
                serializer = ParkingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        gen_response(True, False, "", serializer.data),
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        gen_response(False, True, serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            print(e)
            return Response(
                gen_response(False, True, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )