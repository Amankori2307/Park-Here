from rest_framework import views, status
from rest_framework.response import Response
from .models import User, UserTypeChoices
from utils.utils import check_required_fields, gen_response
from .serializers import ParkingLotSerializer, ParkingLotListSerializer
from .models import ParkingLot
from django.http import Http404

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
            data = ParkingLotListSerializer(serializer.instance).data
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