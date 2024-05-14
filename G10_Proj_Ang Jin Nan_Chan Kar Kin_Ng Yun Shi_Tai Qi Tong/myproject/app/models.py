"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from addproduct.models import Product
from viewproducts.models import Cart


#sharing entity
class Feedback(models.Model):
    feedback_id = models.CharField(primary_key=True, max_length=10)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='customer_feedbacks',to_field='username', limit_choices_to={'username__startswith': 'cst'})
    manager = models.ForeignKey(User, on_delete=models.RESTRICT, null=True,default=None, blank=True,to_field='username', limit_choices_to={'username__startswith': 'mgr'})
    feedback_receive = models.CharField(max_length=255)
    feedback_reply = models.CharField(max_length=255, null=True,default=None, blank=True)
    feedback_date = models.DateTimeField()
    def __str__(self):
        return str(self.feedback_id)

class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=10)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='customer_orders',to_field='username', limit_choices_to={'username__startswith': 'cst'})
    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT, max_length=10)
    staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='staff_orders',to_field='username', limit_choices_to={'username__startswith': 'sstf'})
    order_qty = models.IntegerField()
    order_amt = models.DecimalField(max_digits=5, decimal_places=2)
    order_date = models.DateTimeField()
    order_status = models.TextField()
    delivery_addr = models.TextField()
    delivery_remark = models.TextField(null=True, default=None, blank=True)

    def __str__(self):
        return str(self.order_id)

class OrderItem(models.Model):
    orderItem_id = models.CharField(primary_key=True, max_length=10)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, max_length=10)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='customer_orderitems',to_field='username', limit_choices_to={'username__startswith': 'cst'})
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, max_length=10)
    orderUnitPrice = models.DecimalField(max_digits=5, decimal_places=2)
    orderItem_qty = models.IntegerField()
    orderItem_subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return str(self.orderItem_id)
