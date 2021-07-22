from django.urls import path

from .views import (upload_ihale_view, 
                    ihale_view, 
                    detail_ihale_view, 
                    stock_view,
                    dashboard_view,
                    scrap,
                    upload_anket_view,
                    list_anket_view,
                    list_ikinci_tur_view,
                    detail_ihale_second_tour_view,
                    list_ikinci_tur_supplier_based_view,
                    upload_baglantili_ihale_view,
                    baglantili_ihale_view,
                    detail_baglantili_ihale_view,)

app_name = 'msdepot'

urlpatterns = [
    path('uploadIhale',upload_ihale_view , name = 'upload_ihale_view'),
    path('viewIhale',ihale_view , name = 'ihale_view'),
    path('detailIhale/<int:pk>',detail_ihale_view, name ='detail_ihale_view'),
    path('viewStock',stock_view , name = 'stock_view'),
    path('viewDashboard',dashboard_view , name = 'dashboard_view'),
    path('viewRakipFiyat',scrap , name = 'scrap'),
    path('uploadAnket',upload_anket_view , name = 'upload_anket_view'),
    path('viewAnket',list_anket_view , name = 'list_anket_view'),
    path('viewSecondTour',list_ikinci_tur_view , name = 'list_ikinci_tur_view'),
    path('detailIhaleSecondTour/<int:pk>',detail_ihale_second_tour_view, name ='detail_ihale_second_tour_view'),
    path('viewSecondTourSupplierBased',list_ikinci_tur_supplier_based_view , name = 'list_ikinci_tur_supplier_based_view'),
    path('uploadBaglantiliIhale',upload_baglantili_ihale_view , name = 'upload_baglantili_ihale_view'),
    path('viewBaglantiliIhale',baglantili_ihale_view , name = 'baglantili_ihale_view'),
    path('detailBaglantiliIhale/<int:pk>',detail_baglantili_ihale_view, name ='detail_baglantili_ihale_view'),
    
]