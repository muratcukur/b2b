from django import forms
from .models import SupplierStock

class SupplierStockForm(forms.ModelForm):
    class Meta:
        model = SupplierStock
        fields = ["fruit_vegetable_name"]

        widgets = {'explanation':forms.Textarea(attrs= {'rows': 5})}

        labels = {
            "fruit_vegetable_name" : "Meyve Sebze" ,
            "current_stock" : "Güncel Stok",
            "current_unit" : "Birim(mevcut)",
            "yearly_sales_capacity" : "Yıllık Satış Kapasitesi",
            "yearly_unit" : "Birim(yıllık)",
            "explanation" : "Açıklama",
        }