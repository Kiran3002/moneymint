from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseForbidden
from .models import Stock
from decimal import Decimal
from datetime import date
from django.contrib.auth.decorators import login_required
@login_required
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

        return redirect('stock_list')  # Redirect back to the form

    return render(request, 'admin/add_stocks.html')

import random
import random
from decimal import Decimal
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Stock
from django.contrib.auth.decorators import login_required

@login_required
def update_all_stock_prices(request):
    """
    View to randomly update stock prices by ±5% of their current price.
    """
    if request.method == "POST":
        # Check if the user is an admin
        if not hasattr(request.user, 'role') or request.user.role != "admin":
            return HttpResponseForbidden("You are not authorized to perform this action.")

        try:
            all_stocks = Stock.objects.all()

            for stock in all_stocks:
                # Calculate a random percentage change between -5% and +5%
                percentage_change = Decimal(random.uniform(-3, 4) / 100)
                price_change = stock.latest_price * percentage_change
                new_price = max(Decimal(0), stock.latest_price + price_change)  # Ensure non-negative price

                stock.latest_price = new_price
                stock.last_updated = date.today()
                stock.save()

            return redirect('stock_list')  # Redirect to the stock list page after update
        except Exception as e:
            # Log the exception if needed
            return HttpResponse(f"An error occurred: {e}", status=500)

    return redirect('add_stocks')


from django.shortcuts import render
from django.db.models import Sum, Count, F
from user.models import Payment, Transaction
from authe.models import UserRegistration

def revenue(request):
    """
    Admin dashboard for viewing website revenue, transactions, and user statistics.
    """
    # Total revenue from buy transactions
    total_revenue = Transaction.objects.filter(transaction_type='buy').aggregate(
        revenue=Sum('total_price')
    )['revenue'] or 0

    # Total number of transactions
    total_transactions = Transaction.objects.count()

    # Total funds in user wallets
    total_user_funds = UserRegistration.objects.aggregate(
        total_funds=Sum('funds')
    )['total_funds'] or 0

    # User statistics
    total_users = UserRegistration.objects.filter(role='user').count()
    total_admins = UserRegistration.objects.filter(role='admin').count()

    # Payment analysis
    total_deposits = Payment.objects.filter(payment_type='add').aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_withdrawals = Payment.objects.filter(payment_type='withdraw').aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Recent transactions (limit to 10)
    recent_transactions = Transaction.objects.order_by('-timestamp')[:10]

    # Pass data to the template
    context = {
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'total_user_funds': total_user_funds,
        'total_users': total_users,
        'total_admins': total_admins,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'admin/revenue.html', context)
