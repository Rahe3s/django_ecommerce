# Generated by Django 5.1.1 on 2024-11-12 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_amount',
            new_name='cart_total',
        ),
    ]
