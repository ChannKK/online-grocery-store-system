# Generated by Django 5.0.1 on 2024-02-09 16:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewunassignedorder', '0002_unassignedorder'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UnassignedDeliveryOrder',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('delivery_address', models.CharField(max_length=100)),
                ('items', models.TextField()),
                ('status', models.CharField(choices=[('Unassigned', 'Unassigned'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Unassigned', max_length=20)),
                ('delivery_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UnassignedOrder',
        ),
    ]
