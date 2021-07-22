from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["quantity", "price","destination","destination_bolge","termin","slot","approved"]

        widgets = {'termin': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'})}
        labels = {
            "quantity" : "Miktar",
            "price" : "Birim Fiyatı",
            "destination" : "Gideceği Adresi Tipi",
            "destination_bolge" : "Gideceği Bölge Adı",
            "termin" : "İstenen Tarih",
            "slot":"Saat Aralığı",
            "total_price":"Toplam Fiyat",
            "approved" : "Onaylıyor musunuz ?",
        }