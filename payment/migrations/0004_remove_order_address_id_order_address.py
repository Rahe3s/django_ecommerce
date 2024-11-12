# Generated by Django 5.1.1 on 2024-11-12 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_address_created_at'),
        ('payment', '0003_rename_address_order_address_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address_id',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.address'),
        ),
    ]
