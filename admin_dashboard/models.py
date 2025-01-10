from django.db import models
from datetime import date

class Stock(models.Model):
    symbol = models.CharField(max_length=20, unique=True, help_text="Unique stock symbol")
    name = models.CharField(max_length=100, help_text="Name of the stock")
    latest_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Latest price of the stock")
    last_updated = models.DateField(default=date.today, help_text="Last updated date")

    def __str__(self):
        return f"{self.name} ({self.symbol})"
