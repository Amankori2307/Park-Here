from django.conf.urls import url
from . import views


urlpatterns = [
    # Customer Urls
    url(r'^api/customer/$', views.CustomerListView.as_view()),
    url(r'^api/customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view()),
    url(r'^api/customer/user/$', views.GetSelfDetails.as_view()),

    # Vehicle Urls
    url(r'^api/vehicle/$', views.VehicleListView.as_view()),
    url(r'^api/vehicle/(?P<pk>\d+)/$', views.VehicleDetailView.as_view()),
    
]
