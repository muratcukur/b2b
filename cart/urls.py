from django.urls import path

from .views import upload_order_view

app_name = 'cart'

urlpatterns = [
	path('uploadOrder/<str:supplier>/<str:fruit_vegetable>',upload_order_view , name = 'upload_order_view'),
]