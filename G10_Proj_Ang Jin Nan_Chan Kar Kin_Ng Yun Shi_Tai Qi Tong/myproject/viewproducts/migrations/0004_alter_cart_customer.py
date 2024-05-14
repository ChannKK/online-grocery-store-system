# Generated by Django 5.0.1 on 2024-02-11 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewproducts', '0003_rename_cart_id_cartitem_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(limit_choices_to={'username__startswith': 'cst'}, on_delete=django.db.models.deletion.RESTRICT, related_name='customer_carts', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
