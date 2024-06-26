# Generated by Django 5.0.1 on 2024-02-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewunassignedorder', '0007_deliveryorder_delivery_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryorder',
            name='items',
        ),
        migrations.RemoveField(
            model_name='deliveryorder',
            name='status',
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='delivery_status',
            field=models.CharField(choices=[('Unassigned', 'Unassigned'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Completed', 'Completed')], default='Unassigned', max_length=20),
        ),
    ]
