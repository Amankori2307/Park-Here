from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^api/parking-lot/$', views.ParkingLotListView.as_view()),
    url(r'^api/parking-lot/(?P<pk>\d+)/$', views.ParkingLotDetailView.as_view()),
    url(r'^api/parking-lot/user/$', views.GetSelfDetails.as_view()),


    # Charges
    url(r'^api/charges/$', views.ChargesListView.as_view()),
    url(r'^api/charges/(?P<pk>\d+)/$', views.ChargesDetailView.as_view()),

    # Parking
    url(r'^api/parking/$', views.ParkingListView.as_view()),
    url(r'^api/parking/check-status/(?P<vehicle_ref>\d+)/$', views.GetParkingStatus.as_view()),
    url(r'^api/parking/update-status/(?P<vehicle_ref>\d+)/$', views.UpdateParkingStatus.as_view()),

]
