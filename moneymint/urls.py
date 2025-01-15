
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('authe.urls')),
    path('user/',include('user.urls')),
    path('admin/',include('admin_dashboard.urls')),
]
