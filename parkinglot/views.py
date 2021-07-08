from datetime import datetime, timedelta, timezone
from customer.serializers import CustomerListSerializer
from customer.models import Customer, Vehicle, VehicleTypeChoices
from re import error, search
from utils.permissions import ChargesDetailPermissions, ChargesListPermissions, IsParkingLot
from rest_framework import request, serializers, views, status
from rest_framework.response import Response
from .models import Charges, Parking, PaymentMethodChoices, User, UserTypeChoices
from utils.utils import check_required_fields, gen_response, get_avalable_slots
from .serializers import ParkingListSerializer, ParkingLotSerializer, ParkingLotListSerializer, ChargesSerializer, ParkingSerializer, TransactionSerializer
from .models import ParkingLot
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, OperandHolder
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
import math
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
            if user.user_type != UserTypeChoices.PARKING_LOT:
                return Response(
                    gen_response(True, False, "User Already Exists"),
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            print(e)
            return Response(
                gen_response(False, True, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ParkingLotDetailView(views.APIView):
    def get_object(self, pk):
        try:
            obj = ParkingLot.objects.get(pk=pk)
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
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            token = token[0]
            if user.user_type == UserTypeChoices.CUSTOMER:
                customer = Customer.objects.get(user=user.id)
                serializer = CustomerListSerializer(customer)
            elif user.user_type == UserTypeChoices.PARKING_LOT:
                parking_lot = ParkingLot.objects.get(user=user.id)
                serializer = ParkingLotListSerializer(parking_lot)
            
            data = {
                "auth_token": token.key,
                "user": serializer.data
            }
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
    permission_classes = [IsParkingLot]

    def post(self, request):
        # try:
            errors = check_required_fields(request.data, ["vehicle_ref"])
            if len(errors.keys()):
                return Response(
                    gen_response(True, False, errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Check if there is already an active parking for given vehicle in given parking
            vehicle_ref = request.data.get("vehicle_ref", None)
            parking_lot_ref = request.user.id
            
            parking = Parking.objects.filter(vehicle_ref=vehicle_ref, parking_lot_ref=parking_lot_ref, payment_status=False).order_by("-entry_time")
            if len(parking):
                # serializer = ParkingSerializer(parking, many=True)
                return Response(
                    gen_response(True, False, "This Vehicle Is Already Parked In This Parking Lot, Please Complete Previous Transaction To Start A New One."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Get Vehicle
                try:
                    vehicle = Vehicle.objects.get(pk=vehicle_ref)
                except ParkingLot.DoesNotExist:
                    return Response(
                        gen_response(True, False, "Something Went Wrong"),
                        status=status.HTTP_400_BAD_REQUEST
                    )


                chargesList  = Charges.objects.filter(parking_lot_ref=parking_lot_ref)
                chargesAvailableForVehicles = [ item.vehicle_type for item in chargesList]
                if vehicle.vehicle_type not in chargesAvailableForVehicles:
                    return Response(
                        gen_response(True, False, f"Can't Create Entry For {VehicleTypeChoices.choices[vehicle.vehicle_type][1]}, Because Parking Charges For This Type Of Vehicle Is Not Available  In This Parking Lot(parking_lot_ref: {parking_lot_ref})")
                    )
                
                try:
                    parking_lot = ParkingLot.objects.get(pk=parking_lot_ref)
                except ParkingLot.DoesNotExist:
                    return Response(
                        gen_response(True, False, "Something Went Wrong"),
                        status=status.HTTP_400_BAD_REQUEST
                    )

                availabel_slotes = get_avalable_slots(parking_lot_ref, parking_lot.total_parking_slots)
                if availabel_slotes <= 0:
                    return Response(
                        gen_response(True, False, "0 Available Slots"),
                        status=status.HTTP_400_BAD_REQUEST
                    )

                req_data = request.data
                req_data["parking_lot_ref"] = parking_lot_ref
                serializer = ParkingSerializer(data=req_data)
                if serializer.is_valid():
                    serializer.save()
                    data =  ParkingListSerializer(serializer.instance).data
                    return Response(
                        gen_response(True, False, "", data),
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        gen_response(False, True, serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST
                    )
        # except Exception as e:
        #     return Response(
        #         gen_response(False, True, "Something Went Wrong"),
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

class GetParkingStatus(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsParkingLot]
    def get(self, request, vehicle_ref):
        try:
            parking = Parking.objects.filter(vehicle_ref=vehicle_ref, parking_lot_ref=request.user.id, payment_status=False).order_by("-entry_time")
            if len(parking):
                parking = parking[0]
                serializer = ParkingListSerializer(parking)
                return Response(
                    gen_response(False, True, "", serializer.data),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    gen_response(True, False, "Pakring Entry Does Not Exist"),
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                gen_response(True, False, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class UpdateParkingStatus(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsParkingLot]
    def put(self, request, vehicle_ref):
        try:
            parking = Parking.objects.filter(vehicle_ref=vehicle_ref, parking_lot_ref=request.user.id, payment_status=False).order_by("-entry_time")
            if len(parking):
                
                parking = parking[0]
                data = {
                    "payment_status": True,
                    "exit_time": datetime.now()
                }
                serializer = ParkingSerializer(parking, data=data, partial=True)
                if serializer.is_valid():
                    # Create Transaction
                    try:
                        # Calculate Amount
                        # Pending
                        try:
                            charges = Charges.objects.get(vehicle_type=parking.vehicle_ref.vehicle_type, parking_lot_ref=parking.parking_lot_ref)
                        except Charges.DoesNotExist:
                            return Response(
                                gen_response(True, False, "Charges Not Found"),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            ) 
                        time_diff = datetime.now() - parking.entry_time
                        total_seconds = time_diff.total_seconds()
                        total_minutes = int(total_seconds/60)
    
                        hours = total_minutes//60
                        minutes = total_minutes%60

                        print(f"{hours} hours {minutes} minutes")
                        amount = charges.charges_per_hour * (total_seconds/(60*60))
                        amount = round(amount)
                        transaction_data = {
                            "parking_ref": parking.id,
                            "payment_method": PaymentMethodChoices.COD,
                            "amount": amount
                        }
                        serializedTransaction = TransactionSerializer(data=transaction_data)
                        if serializedTransaction.is_valid():
                            serializedTransaction.save()
                        else:
                            return Response(
                                gen_response(True, False, serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST
                            )    

                    except Exception as e:
                        print(e)
                        return Response(
                            gen_response(True, False, "Something Went Wrong"),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    serializer.save()
                    data =  ParkingListSerializer(serializer.instance).data
                    return Response(
                        gen_response(False, True, "Payment done successfully", data),
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        gen_response(False, True, serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    gen_response(True, False, "Pakring Entry Does Not Exist"),
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            print(e)
            return Response(
                gen_response(True, False, "Something Went Wrong"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
