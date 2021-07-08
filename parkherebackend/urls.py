"""parkherebackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from parkinglot.views import LoginView
from rest_framework import permissions
# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Park Here APIs",
      default_version='v1',
      description="This is the documentation for Park Here APIs, Park Here is a Hybrid(Software + Hardware) solution for handling parking, to reduce paper usage and automate the parking process.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="developer.amankori@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parkinglot.urls')),
    path('', include('customer.urls')),
    path('api/login/', LoginView.as_view()),
    path('chat/', include('chat.urls')),
]
urlpatterns.extend([
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
])