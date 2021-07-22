from django.urls import path

from .views import upload_stock_view, stock_view, order_view, edit_order_view, ajax_edit_order_view

app_name = 'mssupplier'

urlpatterns = [
    path('uploadStock',upload_stock_view , name = 'upload_stock_view'),
    path('viewStock',stock_view , name = 'stock_view'),
    path('viewOrder',order_view , name = 'order_view'),
    path('editOrder/<int:order_id>',edit_order_view , name = 'edit_order_view'),
    path('ajaxEditOrder',ajax_edit_order_view , name = 'ajax_edit_order_view'),
    
]