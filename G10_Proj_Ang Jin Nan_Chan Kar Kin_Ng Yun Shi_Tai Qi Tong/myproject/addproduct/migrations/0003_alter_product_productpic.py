# Generated by Django 4.2.9 on 2024-02-06 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addproduct', '0002_alter_product_productpic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productPic',
            field=models.TextField(blank=True, null=True),
        ),
    ]
