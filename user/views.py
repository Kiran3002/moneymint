from django.shortcuts import render,redirect, get_object_or_404
from admin_dashboard.models import Stock
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authe.models import UserRegistration
from user.models import Payment,Transaction

@login_required
def user_dashboard(request):
    return render(request, 'user/index.html')
def stock_list(request):
    """
    Display all stocks on the stock list page.
    """
    stocks = Stock.objects.all()  # Query all stocks
    return render(request, 'user/stocks.html', {'stocks': stocks})


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal  # Ensures precision in financial calculations

@login_required
def buy_stock(request, stock_id):
    """
    Handles the stock purchase process for the logged-in user.
    """
    # Ensure the logged-in user's data is fetched
    user = get_object_or_404(UserRegistration, email=request.user.email)
    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':
        try:
            # Validate quantity input
            quantity = int(request.POST.get('quantity', 0))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect('buy_stock', stock_id=stock.id)

        # Calculate the total cost of the stock purchase
        total_price = Decimal(stock.latest_price) * quantity

        # Check if the user has enough funds
        if user.funds < total_price:
            messages.error(request, "Insufficient funds to complete the purchase.")
            return redirect('buy_stock', stock_id=stock.id)

        # Deduct funds and save the user
        user.funds -= total_price
        user.save()

        # Record the transaction
        Transaction.objects.create(
            user=user,
            stock=stock,
            quantity=quantity,
            total_price=total_price,
            transaction_type="buy"
        )

        messages.success(
            request, f"Purchase successful! Bought {quantity} units of {stock.name} for ₹{total_price:.2f}."
        )
        return redirect('buy_stock', stock_id=stock.id)

    # Render the stock buying page
    return render(request, 'user/buy_stock.html', {'user': user, 'stock': stock})

    
from decimal import Decimal  # Ensure you import Decimal

@login_required
def payment(request):
    """
    Handles payment operations (add/withdraw funds) and displays the user's transaction history.
    """
    # Get the logged-in user's registration details
    user = get_object_or_404(UserRegistration, email=request.user.email)

    if request.method == 'POST':
        # Get form data
        payment_type = request.POST.get('payment_type')
        try:
            # Convert the amount to a Decimal (avoiding float issues)
            amount = Decimal(request.POST.get('amount', 0))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('payment')

        # Handle withdrawal case
        if payment_type == 'withdraw' and user.funds < amount:
            messages.error(request, "Insufficient funds for withdrawal.")
            return redirect('payment')

        # Update user funds based on payment type
        if payment_type == 'add':
            user.funds += amount  # Decimal + Decimal operation
            action = "added"
        elif payment_type == 'withdraw':
            user.funds -= amount  # Decimal - Decimal operation
            action = "withdrawn"
        else:
            messages.error(request, "Invalid payment type.")
            return redirect('payment')

        user.save()

        # Record payment transaction
        Payment.objects.create(
            user=user,
            amount=amount,
            payment_type=payment_type
        )

        # Provide success feedback
        messages.success(
            request, f"Successfully {action} ₹{amount:.2f}."
        )
        return redirect('payment')

    # Fetch transaction history
    payments = Payment.objects.filter(user=user).order_by('-timestamp')

    # Render the payment page
    return render(request, 'user/payment.html', {'user': user, 'payments': payments})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F, DecimalField
from .models import UserRegistration, Transaction, Stock
@login_required
def portfolio(request):
    """
    Renders the portfolio of the logged-in user, showing holdings and profit/loss.
    """
    user = request.user
    holdings = (
        Transaction.objects.filter(user=user, transaction_type='buy')
        .values('stock__symbol', 'stock__name', 'stock__latest_price')
        .annotate(
            total_quantity=Sum('quantity'),
            total_invested=Sum(F('total_price')),
            avg_price=Sum(F('total_price')) / Sum(F('quantity')),
        )
        .filter(total_quantity__gt=0)
    )
    
    for holding in holdings:
        holding['current_value'] = holding['total_quantity'] * holding['stock__latest_price']
        holding['profit_loss'] = holding['current_value'] - holding['total_invested']
        holding['percent_change'] = (holding['profit_loss'] / holding['total_invested']) * 100 if holding['total_invested'] > 0 else 0

    total_profit_loss = sum(h['profit_loss'] for h in holdings)

    return render(request, 'user/portfolio.html', {'holdings': holdings,'total_profit_loss': total_profit_loss})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Stock, UserRegistration, Transaction

@login_required
def sell_stock(request, stock_symbol):
    """
    Handles selling of a stock by the user.
    """
    # Get the logged-in user
    user = request.user

    # Fetch the stock and user's transactions for that stock
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    transactions = Transaction.objects.filter(user=user, stock=stock, transaction_type='buy')

    if request.method == "POST":
        try:
            # Validate the quantity entered by the user
            sell_quantity = int(request.POST.get('quantity', 0))
            if sell_quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect('sell_stock', stock_symbol=stock_symbol)

        # Calculate the total quantity owned by the user
        total_quantity = transactions.aggregate(total=Sum('quantity'))['total'] or 0
        if sell_quantity > total_quantity:
            messages.error(request, "You cannot sell more than you own.")
            return redirect('sell_stock', stock_symbol=stock_symbol)

        # Calculate total price for the sale
        total_sale_price = Decimal(sell_quantity) * stock.latest_price

        # Create a new 'sell' transaction
        Transaction.objects.create(
            user=user,
            stock=stock,
            quantity=sell_quantity,
            total_price=total_sale_price,
            transaction_type='sell'
        )

        # Add the sale amount to the user's funds
        user.funds += total_sale_price
        user.save()

        messages.success(
            request,
            f"Successfully sold {sell_quantity} units of {stock.name} for ₹{total_sale_price:.2f}."
        )
        return redirect('portfolio')

    # Calculate the total quantity of the stock owned by the user
    total_quantity = transactions.aggregate(total=Sum('quantity'))['total'] or 0

    # Render the sell stock page
    return render(request, 'user/sell_stock.html', {
        'stock': stock,
        'total_quantity': total_quantity
    })
