from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Stock
from decimal import Decimal
from datetime import date

def add_or_update_stock(request):
    """
    View to add a new stock or update an existing one.
    """
    if request.method == "POST":
        symbol = request.POST.get("symbol")
        name = request.POST.get("name")
        price = request.POST.get("price")

        try:
            # Convert price to Decimal and validate
            price = Decimal(price)
        except (ValueError, InvalidOperation):
            return HttpResponse("Invalid price value.", status=400)

        # Retrieve or create the stock, and always update the latest_price
        stock, created = Stock.objects.get_or_create(symbol=symbol, defaults={'name': name, 'latest_price': price})
        if not created:  # If the stock already exists, update its details
            stock.name = name
            stock.latest_price = price
            stock.last_updated = date.today()
            stock.save()

        return redirect('user_dashboard')  # Redirect back to the form

    return render(request, 'admin/add_stocks.html')

import random

def update_all_stock_prices(request):
    """
    View to randomly update stock prices by ±10 points.
    """
    if request.method == "POST":
        try:
            all_stocks = Stock.objects.all()

            for stock in all_stocks:
                # Generate a random price change
                price_change = Decimal(random.uniform(-10, 10))
                new_price = max(Decimal(0), stock.latest_price + price_change)  # Ensure non-negative price

                # Update stock
                stock.latest_price = new_price
                stock.last_updated = date.today()
                stock.save()

            return redirect('add_or_update_stock')  # Redirect to a desired page
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    return redirect('add_or_update_stock')  # Redirect if accessed via GET
