from django.db import models
from django.contrib.auth.models import User
from addproduct.models import Product
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(primary_key=True, max_length=10)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='customer_carts',to_field='username', limit_choices_to={'username__startswith': 'cst'})
    cart_amt = models.DecimalField(max_digits=5, decimal_places=2)
    cart_qty = models.IntegerField()

    def __str__(self):
        return str(self.cart_id)

class CartItem(models.Model):
    cartItem_id = models.CharField(primary_key=True, max_length=10)
    cartItem_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    cartUnitPrice = models.DecimalField(max_digits=5, decimal_places=2)
    cartItem_subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.cartItem_id)