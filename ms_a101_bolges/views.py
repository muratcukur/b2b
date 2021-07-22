from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DepotOrderForm, LocalSupplierOrderForm
from .models import DepotOrder, LocalSupplierOrder
from cart.models import Order
from mssupplier.models import SupplierStock
from msdepot.forms import SearchFruitVegetableForm
from django.http import HttpResponse
import json

# Create your views here.

@login_required
def upload_depotOrder_view(request):
    success_message = None
    error_message = None
    form = DepotOrderForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit = False)
        obj.depot_name = request.user
        obj.user_name = request.user
        obj.save()

        form = DepotOrderForm()

    context = {
    'form' : form,
    'success_message' : success_message,
    'error_message' : error_message,
    }

    return render(request, 'ms_a101_bolges/uploadDepotOrder.html',context)


@login_required
def depotOrder_view(request):
    success_message = None
    error_message = None

    depotOrder = DepotOrder.objects.all()
    
    context = {
    'depotOrder' : depotOrder,
    }

    return render(request, 'ms_a101_bolges/viewDepotOrder.html',context)

@login_required
def depotOrder_view_depot_based(request):
    success_message = None
    error_message = None

    depotOrder = Order.objects.filter(destination_bolge = request.user.username)

    depotBasedOrder = LocalSupplierOrder.objects.filter(destination_bolge = request.user.username)

    bölge = request.user.username

    context = {
    'depotOrder' : depotOrder,
    'depotBasedOrder' : depotBasedOrder,
    'bölge' : bölge,
    }

    return render(request, 'ms_a101_bolges/viewDepotBasedOrder.html',context)

def stock_view(request):
    success_message = None
    error_message = None
    search_stocks= None
    response_data = {}
   
    stocks = SupplierStock.objects.all()
    unique_fruit_vegetable = SupplierStock.objects.order_by("fruit_vegetable_name").values('fruit_vegetable_name').distinct()

    form = LocalSupplierOrderForm(request.POST or None, request.FILES or None)
    form_search = SearchFruitVegetableForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if 'order_sub' in request.POST or request.is_ajax():
            form = LocalSupplierOrderForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.supplier = request.POST.get('supplier_name')
                obj.product = request.POST.get('fruit_vegetable')
                obj.save()
                form = LocalSupplierOrderForm()

            response_data["message"] = "success"

            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else:
            form = LocalSupplierOrderForm()        

        if 'search_fruit_vegetable_sub' in request.POST:
            form_search = SearchFruitVegetableForm(request.POST, request.FILES)
            if form_search.is_valid():
                fruit_vegetable = request.POST['fruit_vegetable_name']
                search_stocks = SupplierStock.objects.all().filter(fruit_vegetable_name = fruit_vegetable)
                form_search = SearchFruitVegetableForm()
        else:
            form_search = SearchFruitVegetableForm()


    context = {
    'form' : form,
    'form_search' : form_search,
    'stocks' : stocks,
    'unique_fruit_vegetable':unique_fruit_vegetable,
    'search_stocks':search_stocks,
    }

    return render(request, 'ms_a101_bolges/viewStock.html',context)