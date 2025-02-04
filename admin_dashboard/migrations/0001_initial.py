# Generated by Django 5.1.4 on 2025-01-10 04:10

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_id', models.CharField(max_length=20, unique=True)),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StockUpdate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.stock')),
            ],
        ),
    ]
