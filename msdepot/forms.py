from django import forms
from .models import IhaleYeni, IhaleTeklif, TedarikciAnket, IhaleIkinciTur, IhaleIkinciTurTeklif, MeyveSebzeYeni, BaglantiliUrunIhalesi, BaglantiliIhaleTeklif
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget

class IhaleForm(forms.ModelForm):

    class Meta:
        model = IhaleYeni

        fields = ["fruit_vegetable_kod", "fruit_vegetable_name", "quantity", "kasa_ebati","paletteki_kasa_sayisi","palet_olcusu","teslim_tarihi",
        "ihale_end_date","spekt_aciklama","sevk_kosullari","koli_kosullari", "hedef_fiyat"]

        widgets = {'ihale_end_date': forms.DateInput(format=('%Y-%m-%d %h-%m'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'}),
                    'teslim_tarihi': forms.DateInput(format=('%Y-%m-%d %h-%m'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'}),
                    'spekt_aciklama': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    'sevk_kosullari': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
                    'koli_kosullari': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
                    }

        labels = {
            "fruit_vegetable_kod" : "Meyve Sebze Kodu" ,
            "fruit_vegetable_name" : "Meyve Sebze Adı" ,
            "quantity" : "Miktar",
            "teslim_tarihi" : "Teslim Tarihi",
            "ihale_end_date" : "İhale Bitiş Tarihi",
            "kasa_ebati" : "Kasa Ebatı",
            "paletteki_kasa_sayisi" : "Paletteki Kasa Sayısı",
            "palet_olcusu" : "Palet Ölçüsü",
            "spekt_aciklama" : "Spekt Açıklama",
            "koli_kosullari" : "Koli Koşulları",
            "hedef_fiyat" : "Hedef Birim Fiyat",

        }

class BaglantiliUrunIhaleForm(forms.ModelForm):
	class Meta:
		model = BaglantiliUrunIhalesi
		fields = ["fruit_vegetable_name", "urun_icerikleri_standartlari", "koli_icerigi","palet_icerigi","ambalaj_maddesi","sabit_fiyat_garantisi",
        "raf_omru","tat_testi_sonucu","tavsiye","karar", "yorum", "ihale_end_date"]


		widgets = {'ihale_end_date': forms.DateInput(format=('%Y-%m-%d %h-%m'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'}),
                    'urun_icerikleri_standartlari': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    }

		labels = {
            "fruit_vegetable_name" : "Meyve Sebze" ,
            "urun_icerikleri_standartlari" : "Ürün İçerikleri Standartları",
            "koli_icerigi" : "Koli İçeriği",
            "palet_icerigi" : "Palet İçeriği",
            "ambalaj_maddesi" : "Ambalaj Maddesi",
            "sabit_fiyat_garantisi" : "Sabit Fiyat Garantisi",
            "raf_omru" : "Raf Ömrü",
            "tat_testi_sonucu" : "Tat Test Sonucu",
            "tavsiye" : "Tavsiye",
            "karar" : "Karar",
            "yorum" : "Yorum",
            "month" : "Ay",
            "planlanan_hedef_tonaj" : "Planlanan Hedef Tonaj",
            "ihale_end_date" : "İhale Bitiş Tarihi",

        }

class IhaleTeklifForm(forms.ModelForm):
    class Meta:
        model = IhaleTeklif
        fields = ["fiyat"]

        labels = {
            "fiyat" : "Birim Fiyatı Giriniz"
        }

class BaglantiliIhaleTeklifForm(forms.ModelForm):
    class Meta:
        model = BaglantiliIhaleTeklif
        fields = ["month", "planlanan_hedef_tonaj"]

        labels = {
            "month" : "Ay",
            "planlanan_hedef_tonaj" : "Tonajı Giriniz."

        }


class IhaleIkinciTurTeklifForm(forms.ModelForm):
    class Meta:
        model = IhaleIkinciTurTeklif
        fields = ["fiyat"]

        labels = {
            "fiyat" : "Birim Fiyatı Giriniz"
        }

class IhaleIkinciTurForm(forms.ModelForm):
    class Meta:
        model = IhaleIkinciTur

        fields = ["suppliers","ihale_end_date", "hedef_fiyat"]

        widgets = {'ihale_end_date': forms.DateInput(format=('%Y-%m-%d %h-%m'), attrs={'class':'form-control', 'placeholder':'Tarih Seçiniz', 'type':'date'}),}

        labels = {
            "suppliers" : "Tedarikçileri Seçiniz",
            "ihale_end_date" :"İkinci Tur Bitiş Tarihi",
            "hedef_fiyat" : "Hedef Fiyat Seçiniz",
        }

class SearchFruitVegetableForm(forms.Form):

    fruit_vegetable_name = forms.ModelChoiceField(queryset=MeyveSebzeYeni.objects.order_by('fruit_vegetable_name_yeni').all(), label='Meyve Sebze Adı')


class TedarikciAnketForm(forms.ModelForm):
    class Meta:
        model = TedarikciAnket
        fields = ["year", "month", "supplier", "bulunurluk","tazelik","temizlik","duzen","personel_kisisel_bakimi"]

        labels = {
                "year" : "Yıl" ,
                "month" : "Ay",
                "supplier" : "Tedarikçi",
                "bulunurluk" : "Bulunurluk Puan",
                "tazelik" : "Tazelik Puan",
                "temizlik" : "Temizlik Puan",
                "duzen" : "Düzen Puan",
                "personel_kisisel_bakimi" : "Personel Kişisel Bakım Puan",
            }

