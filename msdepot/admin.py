from django.contrib import admin
from .models import IhaleTeklif, RakipFiyatTakip, TedarikciAnket, MeyveSebzeYeni, IhaleYeni, IhaleIkinciTur, IhaleIkinciTurTeklif, BaglantiliUrunIhalesi, BaglantiliIhaleAyHedefTonaj, BaglantiliIhaleTeklif

# Register your models here.

admin.site.register(IhaleYeni)
admin.site.register(IhaleTeklif)
admin.site.register(RakipFiyatTakip)
admin.site.register(TedarikciAnket)
admin.site.register(MeyveSebzeYeni)
admin.site.register(IhaleIkinciTur)
admin.site.register(IhaleIkinciTurTeklif)
admin.site.register(BaglantiliUrunIhalesi)
admin.site.register(BaglantiliIhaleAyHedefTonaj)
admin.site.register(BaglantiliIhaleTeklif)

class IhaleIkinciTurInline(admin.StackedInline):
    model = IhaleIkinciTur

class IhaleYeniAdmin(admin.ModelAdmin):
    inlines = [
        IhaleIkinciTurInline,
    ]
