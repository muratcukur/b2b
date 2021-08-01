from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from jsonfield import JSONField
# Create your models here.

class MeyveSebze(models.Model):
    UNIT_CHOICES = (
        ('Adet', 'Adet'),
        ('Kilo', 'Kilo'),
    )
    meyve_sebze_adi = models.CharField(max_length=50)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    def __str__(self):
        return str(self.id)

class MeyveSebzeYeni(models.Model):
    UNIT_CHOICES = (
        ('Adet', 'Adet'),
        ('Kilo', 'Kilo'),
    )
    fruit_vegetable_kod_yeni = models.IntegerField(default = None, blank = True, null = True)
    fruit_vegetable_name_yeni = models.CharField(max_length=50)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    def __str__(self):
        return str(self.fruit_vegetable_kod_yeni)

class Ihale(models.Model):

    #EBAT_CHOICES = (
    #    ('30x40x15', '30x40x15'),
     #   ('20x30x20', '20x30x20'),
    #)
    #PALET_OLCUSU = (
    #    ("euro", "euro"),
    #    ("dusseldorf", "dusseldorf"),
    #)
    fruit_vegetable_name = models.CharField(max_length=50)

    quantity = models.FloatField()
    #kasa_ebati = models.CharField(max_length=30, choices = EBAT_CHOICES)
    #paletteki_kasa_sayisi = models.IntegerField()
    #palet_olcusu = models.CharField(max_length=10, choices = PALET_OLCUSU)
    #unit = models.CharField(max_length=10)
    #teslim_tarihi = models.DateTimeField(auto_now_add = False)
    ihale_date = models.DateTimeField(auto_now_add = True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    ihale_end_date = models.DateField(auto_now_add = False)
    #spekt_aciklama = models.CharField(max_length=300)
    #sevk_kosullari = models.CharField(max_length=50)
    #koli_kosullari = models.CharField(max_length=50)
    
    #def save(self, *args, **kwargs):
     #   self.unit = MeyveSebze.objects.filter(fruit_vegetable_name=self.fruit_vegetable_name).values("unit")
     #   super(Ihale, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class IhaleYeni(models.Model):

    EBAT_CHOICES = (
        ('30x40x15', '30x40x15'),
        ('20x30x20', '20x30x20'),
    )
    PALET_OLCUSU = (
        ("euro", "euro"),
        ("dusseldorf", "dusseldorf"),
    )
    fruit_vegetable_kod = models.ForeignKey(MeyveSebzeYeni, on_delete=models.CASCADE)
    fruit_vegetable_name = models.CharField(max_length=30)
    quantity = models.FloatField()
    kasa_ebati = models.CharField(max_length=30, choices = EBAT_CHOICES)
    paletteki_kasa_sayisi = models.IntegerField()
    palet_olcusu = models.CharField(max_length=10, choices = PALET_OLCUSU)
    unit = models.CharField(max_length=10)
    teslim_tarihi = models.DateTimeField(auto_now_add = False)
    ihale_date = models.DateTimeField(auto_now_add = True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    ihale_end_date = models.DateField(auto_now_add = False)
    spekt_aciklama = models.CharField(max_length=300)
    sevk_kosullari = models.CharField(max_length=50)
    koli_kosullari = models.CharField(max_length=50)
    hedef_fiyat = models.FloatField(null=True, blank=True, default=None)
    
    def save(self, *args, **kwargs):
        self.unit = MeyveSebzeYeni.objects.filter(fruit_vegetable_name_yeni=self.fruit_vegetable_name).values("unit")
        super(IhaleYeni, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class IhaleIkinciTur(models.Model):

    ihale_id = models.ForeignKey(IhaleYeni, on_delete=models.CASCADE)
    suppliers = models.ManyToManyField(User)
    ihale_end_date = models.DateTimeField(auto_now_add = False)
    hedef_fiyat = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.ihale_id)

class IhaleTeklif(models.Model):
    ihale_id = models.ForeignKey(IhaleYeni, on_delete=models.CASCADE)
    tedarikci = models.ForeignKey(User, on_delete=models.CASCADE)
    ihale_teklif_date = models.DateTimeField(auto_now_add = True)
    fiyat = models.FloatField()

    def __str__(self):
        return str(self.id)

class IhaleIkinciTurTeklif(models.Model):
    ihale_id = models.ForeignKey(IhaleYeni, on_delete=models.CASCADE)
    tedarikci = models.ForeignKey(User, on_delete=models.CASCADE)
    ihale_teklif_date = models.DateTimeField(auto_now_add = True)
    fiyat = models.FloatField()

    def __str__(self):
        return str(self.id)

class BaglantiliUrunIhalesi(models.Model):

    MONTH_CHOICES = (
        ('Ocak', 'Ocak'),
        ('Şubat', 'Şubat'),
        ('Mart', 'Mart'),
        ('Nisan', 'Nisan'),
        ('Mayıs', 'Mayıs'),
        ('Haziran', 'Haziran'),
        ('Temmuz', 'Temmuz'),
        ('Ağustos', 'Ağustos'),
        ('Eylül', 'Eylül'),
        ('Ekim', 'Ekim'),
        ('Kasım', 'Kasım'),
        ('Aralık', 'Aralık'),
    )

    fruit_vegetable_name = models.ForeignKey(MeyveSebzeYeni, on_delete=models.CASCADE)
    urun_icerikleri_standartlari = models.CharField(max_length = 220, null=True, blank=True, default=None)
    koli_icerigi = models.CharField(max_length = 50, null=True, blank=True, default=None)
    palet_icerigi = models.CharField(max_length = 50, null=True, blank=True, default=None)
    ambalaj_maddesi = models.CharField(max_length = 50, null=True, blank=True, default=None)
    sabit_fiyat_garantisi = models.CharField(max_length = 50, null=True, blank=True, default=None)
    raf_omru = models.CharField(max_length = 50, null=True, blank=True, default=None)
    tat_testi_sonucu = models.CharField(max_length = 50, null=True, blank=True, default=None)
    tavsiye = models.CharField(max_length = 50, null=True, blank=True, default=None)
    karar = models.CharField(max_length = 50, null=True, blank=True, default=None)
    yorum = models.CharField(max_length = 50, null=True, blank=True, default=None)
    month = models.CharField(max_length=15, choices=MONTH_CHOICES, null=True, blank=True, default=None)
    planlanan_hedef_fiyat = models.FloatField(null=True, blank=True, default=None)
    planlanan_hedef_tonaj = models.FloatField(null=True, blank=True, default=None)
    ihale_end_date = models.DateField(auto_now_add = False)

    def __str__(self):
        return str(self.id)

class BaglantiliIhaleAyHedefTonaj(models.Model):
    baglantiliihaleid = models.ForeignKey(BaglantiliUrunIhalesi, on_delete=models.CASCADE)
    month = models.CharField(max_length = 50, null=True, blank=True, default=None)
    planlanan_hedef_fiyat = models.FloatField(null=True, blank=True, default=None)
    planlanan_hedef_tonaj = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return "Bağlantılı ürün ihale ay hedef tonaj:%s Bağlantılı ürün ihale id:%s" % (self.id, self.baglantiliihaleid )

class BaglantiliIhaleTeklif(models.Model):
    baglantiliihaleid = models.ForeignKey(BaglantiliUrunIhalesi, on_delete=models.CASCADE)
    tedarikci = models.ForeignKey(User, on_delete=models.CASCADE)
    ihale_teklif_date = models.DateTimeField(auto_now_add = True)
    month = models.CharField(max_length = 50, null=True, blank=True, default=None)
    planlanan_hedef_fiyat = models.FloatField(null=True, blank=True, default=None)
    planlanan_hedef_tonaj = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)

class RakipFiyatTakip(models.Model):
    fruit_vegetable_name = models.CharField(max_length = 30)
    price = models.CharField(max_length = 10)
    rakip = models.CharField(max_length = 10)
    indirim = models.CharField(max_length = 20)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.fruit_vegetable_name)

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class TedarikciAnket(models.Model):
    
    MONTH_CHOICES = (
        ('Ocak', 'Ocak'),
        ('Şubat', 'Şubat'),
        ('Mart', 'Mart'),
        ('Nisan', 'Nisan'),
        ('Mayıs', 'Mayıs'),
        ('Haziran', 'Haziran'),
        ('Temmuz', 'Temmuz'),
        ('Ağustos', 'Ağustos'),
        ('Eylül', 'Eylül'),
        ('Ekim', 'Ekim'),
        ('Kasım', 'Kasım'),
        ('Aralık', 'Aralık'),
    )

    PUAN_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(2015), max_value_current_year])
    month = models.CharField(max_length=15, choices=MONTH_CHOICES)
    supplier = models.CharField(max_length = 50)
    bulunurluk = models.CharField(max_length=5, choices=PUAN_CHOICES)
    tazelik = models.CharField(max_length=5, choices=PUAN_CHOICES)
    temizlik = models.CharField(max_length=5, choices=PUAN_CHOICES)
    duzen = models.CharField(max_length=5, choices=PUAN_CHOICES)
    personel_kisisel_bakimi = models.CharField(max_length=5, choices=PUAN_CHOICES)
    anket_date = models.DateTimeField(auto_now_add = True)
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.supplier)



