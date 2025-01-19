from django.db import models
from authe.models import UserRegistration
from admin_dashboard.models import Stock

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('add', 'Add Funds'),
        ('withdraw', 'Withdraw Funds'),
    ]

    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.payment_type} {self.amount} at {self.timestamp}"
    

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name="transactions")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="transactions")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES,default='buy')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.stock.name} ({self.quantity} units, {self.transaction_type})"


