
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authe.urls')),
    path('user',include('user.urls')),
    
]
