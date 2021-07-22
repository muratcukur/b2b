from django.db import models
from django.contrib.auth.models import User
from msdepot.models import MeyveSebzeYeni

# Create your models here.

class SupplierStock(models.Model):
    UNIT_CHOICES = (
        ('Adet', 'Adet'),
        ('Kilo', 'Kilo'),
    )
    supplier_name = models.ForeignKey(User, on_delete=models.CASCADE)
    fruit_vegetable_name = models.ForeignKey(MeyveSebzeYeni, on_delete=models.CASCADE)
    current_stock = models.FloatField(null=True, blank = True)
    current_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, null=True, blank = True)
    yearly_sales_capacity = models.FloatField(null=True, blank = True)
    yearly_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, null=True, blank = True)
    explanation = models.CharField(max_length=200, null=True, blank = True)
    

    def __str__(self):
        return str(self.supplier_name)