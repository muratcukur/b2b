from django import forms
from .models import DepotOrder, LocalSupplierOrder

class DepotOrderForm(forms.ModelForm):
    class Meta:
        model = DepotOrder
        fields = ["fruit_vegetable_name", "palet", "teslim_tarihi"]
  
        widgets = {'teslim_tarihi': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'})}

        labels = {
            #"depot_name": "Depo Seçiniz" ,
            "fruit_vegetable_name" : "Meyve Sebze" ,
            "palet" : "Palet",
            #"unit" : "Birim",
            "teslim_tarihi" : "Teslim Tarihi",
        }

class LocalSupplierOrderForm(forms.ModelForm):
    class Meta:
        model = LocalSupplierOrder
        fields = ["quantity","termin","slot","approved"]

        widgets = {'termin': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'})}

        labels = {
            "quantity" : "Palet",
            "termin" : "İstenen Tarih",
            "slot":"Saat Aralığı",
            "total_price":"Toplam Fiyat",
            "approved" : "Onaylıyor musunuz ?",
        }