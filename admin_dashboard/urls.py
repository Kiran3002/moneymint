from django.contrib import admin
from django.urls import path
from .views import add_or_update_stock,update_all_stock_prices,revenue
urlpatterns = [
    
    path('add_stocks', add_or_update_stock, name='add_stocks'),
    path('update_stock',update_all_stock_prices, name='update_stock'),
    path('admin/', admin.site.urls),
    path('revenue/', revenue, name='revenue'),
]