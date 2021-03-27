from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^api/parking-lot/$', views.ParkingLotListView.as_view()),
    url(r'^api/parking-lot/(?P<pk>\d+)/$', views.ParkingLotDetailView.as_view()),
    url(r'^api/parking-lot/user/$', views.GetSelfDetails.as_view()),
]
