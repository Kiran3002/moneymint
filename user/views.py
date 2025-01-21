from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, Case, When, DecimalField, ExpressionWrapper,Q
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from .models import Stock, UserRegistration, Transaction,Payment
from django.db import transaction as db_transaction



@login_required
def user_dashboard(request):
    return render(request, 'user/index.html')
def stock_list(request):

    stocks = Stock.objects.all()  
    return render(request, 'user/stocks.html', {'stocks': stocks})

@login_required
def buy_stock(request, stock_id):
    
    user = get_object_or_404(UserRegistration, email=request.user.email)
    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect('buy_stock', stock_id=stock.id)

        total_price = Decimal(stock.latest_price) * quantity

        if user.funds < total_price:
            messages.error(request, "Insufficient funds to complete the purchase.")
            return redirect('buy_stock', stock_id=stock.id)

        user.funds -= total_price
        user.save()

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
        return redirect('portfolio')

    return render(request, 'user/buy_stock.html', {'user': user, 'stock': stock})

@login_required
def payment(request):
    
    user = get_object_or_404(UserRegistration, email=request.user.email)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        try:
            amount = Decimal(request.POST.get('amount', 0))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('payment')
        if payment_type == 'withdraw' and user.funds < amount:
            messages.error(request, "Insufficient funds for withdrawal.")
            return redirect('payment')

        if payment_type == 'add':
            user.funds += amount  
            action = "added"
        elif payment_type == 'withdraw':
            user.funds -= amount  
            action = "withdrawn"
        else:
            messages.error(request, "Invalid payment type.")
            return redirect('payment')

        user.save()

        Payment.objects.create(
            user=user,
            amount=amount,
            payment_type=payment_type
        )

        messages.success(
            request, f"Successfully {action} ₹{amount:.2f}."
        )
        return redirect('payment')

    payments = Payment.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'user/payment.html', {'user': user, 'payments': payments})


@login_required
def portfolio(request):
  
  user = request.user

  holdings = (
      Transaction.objects.filter(user=user)
      .values('stock__symbol', 'stock__name', 'stock__latest_price')
      .annotate(
          total_buy_quantity=ExpressionWrapper(
              Sum(Case(When(transaction_type='buy', then=F('quantity'))), default=0),
              output_field=DecimalField()
          ),
          total_sell_quantity=ExpressionWrapper(
              Sum(Case(When(transaction_type='sell', then=F('quantity'))), default=0),
              output_field=DecimalField()
          ),
          total_buy_value=ExpressionWrapper(
              Sum(Case(When(transaction_type='buy', then=F('total_price'))), default=0),
              output_field=DecimalField()
          ),
          total_sell_value=ExpressionWrapper(
              Sum(Case(When(transaction_type='sell', then=F('total_price'))), default=0),
              output_field=DecimalField()
          ),
      )
      .annotate(
          total_quantity=ExpressionWrapper(
              F('total_buy_quantity') - F('total_sell_quantity'),
              output_field=DecimalField()
          ),
          total_invested=ExpressionWrapper(
              F('total_buy_value') - F('total_sell_value'),
              output_field=DecimalField()
          ),
          avg_price=Sum(F('total_price')) / Sum(F('quantity')),
      )
      .filter(total_quantity__gt=0)  
  )

  holdings = list(holdings)
  for holding in holdings:
      latest_price = Decimal(holding['stock__latest_price']) if not isinstance(holding['stock__latest_price'], Decimal) else holding['stock__latest_price']
      holding['current_value'] = holding['total_quantity'] * latest_price
      holding['profit_loss'] = holding['current_value'] - holding['total_invested']
      holding['percent_change'] = (
          (holding['profit_loss'] / holding['total_invested']) * 100
          if holding['total_invested'] > 0 else 0
      )

  total_profit_loss = sum(h['profit_loss'] for h in holdings)

  return render(request, 'user/portfolio.html', {'holdings': holdings, 'total_profit_loss': total_profit_loss})

@login_required
def sell_stock(request, stock_symbol):
    
    user = request.user

    # Fetch the stock and calculate total owned quantity
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    user_transactions = Transaction.objects.filter(user=user, stock=stock)

    # Calculate net quantity owned
    net_quantity = (
        user_transactions.filter(transaction_type='buy').aggregate(total=Sum('quantity'))['total'] or 0
    ) - (
        user_transactions.filter(transaction_type='sell').aggregate(total=Sum('quantity'))['total'] or 0
    )

    if request.method == "POST":
        try:
            sell_quantity = int(request.POST.get('quantity', 0))
            if sell_quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect('sell_stock', stock_symbol=stock_symbol)

        if sell_quantity > net_quantity:
            messages.error(request, "You cannot sell more than you own.")
            return redirect('sell_stock', stock_symbol=stock_symbol)

        total_sale_price = Decimal(sell_quantity) * stock.latest_price

        with db_transaction.atomic():
            Transaction.objects.create(
                user=user,
                stock=stock,
                quantity=sell_quantity,
                total_price=total_sale_price,
                transaction_type='sell'
            )

            user.funds += total_sale_price
            user.save()

        messages.success(
            request,
            f"Successfully sold {sell_quantity} units of {stock.name} for ₹{total_sale_price:.2f}."
        )
        return redirect('portfolio')

    return render(request, 'user/sell_stock.html', {
        'stock': stock,
        'total_quantity': net_quantity
    })
