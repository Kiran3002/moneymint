# Generated by Django 5.1.4 on 2025-01-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0004_alter_userregistration_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userregistration',
            options={},
        ),
        migrations.AddField(
            model_name='userregistration',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
