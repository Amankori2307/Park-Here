from django.conf.urls import url
from . import views


urlpatterns = [


    # Customer Login
    url(r'^api/customer/login/$', views.LoginCustomer.as_view()),

    #GET the all Shoppers details
    # url(r'^api/customers/$', views.ShoppersDetails.as_view()),

    #GET the single Shoppers details
    # url(r'^api/customer/(?P<pk>[0-9a-zA-Z_]+)/$', views.ShopperDetailsByID.as_view()),
    #POST the Shoppers Details
    url(r'^api/customer/add/$', views.InsertCustomer.as_view()),
    #PUT updates single Shopper detail
    # url(r'^api/updatecustomer/(?P<pk>[0-9a-zA-Z_]+)/$', views.UpdateShopper.as_view()),
    #DELETE single Shopper detail
    # url(r'^api/deletecustomer/(?P<pk>[0-9a-zA-Z_]+)/$', views.DeleteShopper.as_view()),
    # GET User Details By Id

    url(r'^api/customerById/$', views.CustomerById.as_view()),
    # Logout User
    # url(r'^api/customer/logout/$', views.LogoutView.as_view()),


]
