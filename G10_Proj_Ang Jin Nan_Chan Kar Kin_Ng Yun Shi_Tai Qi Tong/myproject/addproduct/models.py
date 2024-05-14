from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.CharField(primary_key=True, max_length=10)
    product_name = models.TextField()
    product_price = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    product_qty = models.IntegerField(null=True, blank=True)
    product_info = models.TextField()
    product_pic = models.ImageField(upload_to='product_images/',null=True, blank=True)

    def __str__(self):
        return str(self.product_id)

