from django.urls import path

from .views import upload_depotOrder_view, depotOrder_view, depotOrder_view_depot_based, stock_view

app_name = 'ms_a101_bolges'

urlpatterns = [
	path('uploadDepotOrder',upload_depotOrder_view , name = 'upload_depotOrder_view'),
    path('DepotOrder',depotOrder_view , name = 'depotOrder_view'),
    path('DepotBasedOrder',depotOrder_view_depot_based , name = 'depotOrder_view_depot_based'),
    path('viewStock',stock_view , name = 'stock_view'),
]