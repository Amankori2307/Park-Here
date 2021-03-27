from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api/customer/$', views.CustomerListView.as_view()),
    url(r'^api/customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view()),
]
