from django.contrib import admin
from django.urls import path
from .views import Login_auth,Register_auth
urlpatterns = [
    path('',Login_auth, name='login'),
    path('register/', Register_auth, name='register'),
]
