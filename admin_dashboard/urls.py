from django.contrib import admin
from django.urls import path
from .views import add_or_update_stock
urlpatterns = [
    
    path('add_stocks', add_or_update_stock, name='add_stocks'),
]