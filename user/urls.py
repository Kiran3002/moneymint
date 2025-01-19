from django.contrib import admin
from django.urls import path
from .views import user_dashboard,stock_list,buy_stock,portfolio,sell_stock
from .views import payment
urlpatterns = [
    
    path('user_dashboard', user_dashboard, name='user_dashboard'),
    path('stock_list',stock_list, name='stock_list'),
    path('buy_stock/<int:stock_id>/', buy_stock, name='buy_stock'),  
    path('payment',payment, name='payment'),
    path('portfolio',portfolio, name='portfolio'),
    path('sell/<str:stock_symbol>/', sell_stock, name='sell_stock'),
]