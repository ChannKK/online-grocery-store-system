# Generated by Django 4.2.9 on 2024-02-06 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('productName', models.TextField()),
                ('productPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('productQty', models.IntegerField(blank=True, null=True)),
                ('productInfo', models.TextField()),
                ('productPic', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
