from django.db import models
from django.contrib.auth.models import User
from app.models import models

class DeliveryOrder(models.Model):
    delivery_id = models.CharField(max_length=10)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    delivery_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.CharField(max_length=100, null=True) 
    STATUS_CHOICES = (('Unassigned', 'Unassigned'),('Accepted', 'Accepted'),('Declined', 'Declined'),('Completed', 'Completed'))
    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unassigned')
    delivery_pic = models.ImageField(upload_to='proof_photo/', null=True, blank=True)

    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.delivery_status}"
    
    
