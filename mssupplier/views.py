from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SupplierStockForm
from .models import SupplierStock
from cart.models import Order
from cart.forms import OrderForm
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers

# Create your views here.


@login_required
def upload_stock_view(request):
    success_message = None
    error_message = None
    form = SupplierStockForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit = False)
        obj.supplier_name = request.user
        obj.save()

        form = SupplierStockForm()

    context = {
    'form' : form,
    'success_message' : success_message,
    'error_message' : error_message,
    }

    return render(request, 'mssupplier/uploadStock.html',context)   


def stock_view(request):
    success_message = None
    error_message = None
   

    stocks = SupplierStock.objects.all().filter(supplier_name = request.user)
    
    context = {
    'stocks' : stocks,
    }

    return render(request, 'mssupplier/viewStock.html',context)


def order_view(request):
    success_message = None
    error_message = None
   
    orders = Order.objects.all().filter(supplier = request.user)
    
    context = {
    'orders' : orders,
    }

    return render(request, 'mssupplier/viewOrder.html',context)


def ajax_edit_order_view(request):

    if request.method == "POST":
        if request.is_ajax():

            id1 = request.POST.get('id',None)
            order_edit = Order.objects.get(id = id1)
            order_edit_form = OrderForm(request.POST or None, request.FILES or None, instance = order_edit)
            if order_edit_form.is_valid():

                updated_instance = order_edit_form.save()
                ser_instance = serializers.serialize('json', [ updated_instance , ])

                form = OrderForm()

                return JsonResponse({"instance": ser_instance}, status = 200)
                

def edit_order_view(request, order_id):
    success_message = None
    error_message = None

    order_id = int(order_id)

    order_edit = Order.objects.get(id = order_id)
    order_edit_form = OrderForm(request.POST or None, request.FILES or None, instance = order_edit)

    if request.method == "POST":
        if order_edit_form.is_valid():
            order_edit_form.save()
    
        return redirect('mssupplier:order_view')

    context = {
    'order_edit_form' : order_edit_form,
    }

    return render(request, 'mssupplier/editOrder.html',context)

    