# Generated by Django 5.1.4 on 2025-01-20 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0008_alter_userregistration_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='admin', max_length=10),
        ),
    ]
