from django.contrib import admin

from app.models import Feedback, Order, OrderItem
from viewproducts.models import Cart, CartItem

admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)