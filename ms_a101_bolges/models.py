from django.db import models
from django.contrib.auth.models import User
from msdepot.models import MeyveSebzeYeni

# Create your models here.

class DepotOrder(models.Model):

    depot_name = models.CharField(max_length = 20)
    fruit_vegetable_name = models.ForeignKey(MeyveSebzeYeni, on_delete=models.CASCADE)
    #fruit_vegetable_name = models.CharField(max_length = 20)
    palet = models.FloatField()
    unit = models.CharField(max_length = 20, null = True)
    teslim_tarihi = models.DateTimeField(auto_now_add = False)
    order_date = models.DateTimeField(auto_now_add = True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.unit = MeyveSebzeYeni.objects.filter(fruit_vegetable_name=self.fruit_vegetable_name).values("unit")
        super(DepotOrder, self).save(*args, **kwargs)

    def __str__(self):
        return self.depot_name


class LocalSupplierOrder(models.Model):
    DESTINATION_BOLGE_CHOICES = (
        ('serik', 'serik'),
        ('lüleburgaz', 'lüleburgaz'),
        ('sakarya', 'sakarya'),
    )
    SLOT_CHOICES = (
        ("07:00-12:00","07:00-12:00"),
        ("12:00-19:00","12:00-19:00"),
    )
    UNIT_CHOICES = (
    ('Adet', 'Adet'),
    ('Kilo', 'Kilo'),
    )
    supplier = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price = models.FloatField(default = 0)
    destination_bolge = models.CharField(max_length=30, choices=DESTINATION_BOLGE_CHOICES)
    termin = models.DateTimeField(auto_now_add = False)
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES)
    approved = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)


    def __str__(self):
        return  self.supplier


