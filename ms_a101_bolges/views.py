from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DepotOrderForm, LocalSupplierOrderForm
from .models import DepotOrder, LocalSupplierOrder
from cart.models import Order
from mssupplier.models import SupplierStock
from msdepot.forms import SearchFruitVegetableForm
from django.http import HttpResponse
import json
from django.db import connection
import pandas as pd

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
def urunBazliDepotOrder_view(request):
    tarih = None
    cursor = connection.cursor()

    query = """  select ms.fruit_vegetable_name, sum(msorder.palet) as toplam from ms_a101_bolges_depotorder msorder 
        left join msdepot_meyvesebzeyeni ms on 
        msorder.fruit_vegetable_name_id = ms.id
        group by msorder.fruit_vegetable_name_id  """

    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.description
    cursor.close()
    column = []
    for col in columns:
        column.append(col[0])

    urun_bazli_depot_order = pd.DataFrame(result,columns=column)

    if request.method == "POST":
        cursor = connection.cursor()
        tarih = request.POST.get("teslim_tarihi", "")
        tarih = str(tarih)

        query2 = """  select ms.fruit_vegetable_name, sum(msorder.palet) as toplam from ms_a101_bolges_depotorder msorder 
        left join msdepot_meyvesebzeyeni ms on 
        msorder.fruit_vegetable_name_id = ms.id where DATE(msorder.teslim_tarihi) = %s
        group by msorder.fruit_vegetable_name_id """

        data_tuple=(tarih,)
        cursor.execute(query2,data_tuple)
        result = cursor.fetchall()
        columns = cursor.description
        cursor.close()
        column = []
        for col in columns:
            column.append(col[0])

        urun_bazli_depot_order = pd.DataFrame(result,columns=column)  

    context = {
    'urun_bazli_depot_order' : urun_bazli_depot_order,
    'tarih' : tarih,
    }

    return render(request, 'ms_a101_bolges/viewUrunBazliDepotOrder.html',context)


@login_required
def bolgeBazliDepotOrder_view(request):

    cursor = connection.cursor()

    query = """  select depot_name, sum(palet) as toplam from ms_a101_bolges_depotorder  
            group by depot_name  """

    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.description
    cursor.close()
    column = []
    for col in columns:
        column.append(col[0])

    bolge_bazli_depot_order = pd.DataFrame(result,columns=column)

    if request.method == "POST":
        cursor = connection.cursor()
        tarih = request.POST.get("teslim_tarihi", "")
        tarih = str(tarih)

        query2 = """  select depot_name, sum(palet) as toplam from ms_a101_bolges_depotorder  
            where DATE(teslim_tarihi) = %s
            group by depot_name """

        data_tuple=(tarih,)
        cursor.execute(query2,data_tuple)
        result = cursor.fetchall()
        columns = cursor.description
        cursor.close()
        column = []
        for col in columns:
            column.append(col[0])

        bolge_bazli_depot_order = pd.DataFrame(result,columns=column)  

    context = {
    'bolge_bazli_depot_order' : bolge_bazli_depot_order,
    }

    return render(request, 'ms_a101_bolges/viewBolgeBazliDepotOrder.html',context)

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
                obj.destination_bolge = request.user
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
                search_stocks = SupplierStock.objects.filter(fruit_vegetable_name = fruit_vegetable).first()
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