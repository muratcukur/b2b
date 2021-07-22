from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from msdepot.models import MeyveSebzeYeni
# Create your models here.


class Order(models.Model):
    DESTINATION_CHOICES = (
        ('MsDepo', 'MsDepo'),
        ('Bölge', 'Bölge'),
    )
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
    unit = models.CharField(max_length=10, null=True, blank=True, default=None)
    price = models.FloatField(default = 0)
    destination = models.CharField(max_length=10, choices=DESTINATION_CHOICES)
    destination_bolge = models.CharField(max_length=30, choices=DESTINATION_BOLGE_CHOICES)
    termin = models.DateTimeField(auto_now_add = False)
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES)
    approved = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        self.unit = MeyveSebzeYeni.objects.filter(fruit_vegetable_name=self.product).values("unit")
        super(Order, self).save(*args, **kwargs)


    def __str__(self):
        return  self.supplier
