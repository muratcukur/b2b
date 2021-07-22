from django.contrib import admin
from .models import DepotOrder, LocalSupplierOrder
from django.contrib.auth.models import User

# Register your models here.


admin.site.register(DepotOrder)
admin.site.register(LocalSupplierOrder)
