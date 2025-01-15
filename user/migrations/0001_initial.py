# Generated by Django 5.1.4 on 2025-01-12 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authe', '0003_remove_userregistration_id_userregistration_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('payment_type', models.CharField(choices=[('add', 'Add Funds'), ('withdraw', 'Withdraw Funds')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authe.userregistration')),
            ],
        ),
    ]
