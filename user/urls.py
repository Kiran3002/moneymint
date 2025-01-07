from django.contrib import admin
from django.urls import path
from .views import user_dashboard
urlpatterns = [
    
    path('user_dashboard', user_dashboard, name='user_dashboard'),
]