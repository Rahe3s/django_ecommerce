# Generated by Django 5.1.1 on 2024-11-22 13:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_productvariant_id_productvariant_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]