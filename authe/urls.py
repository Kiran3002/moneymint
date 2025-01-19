from django.contrib import admin
from django.urls import path
from .views import Login_auth,Register_auth,logout_view
urlpatterns = [
    path('',Login_auth, name='login'),
    path('register/', Register_auth, name='register'),
    path('logout/', logout_view, name='logout'),
]
