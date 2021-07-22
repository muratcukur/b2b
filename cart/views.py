from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order
from datetime import date

# Create your views here.

@login_required
def upload_order_view(request, supplier, fruit_vegetable):
    success_message = None
    error_message = None

    return render(request, 'msdepot/viewStock.html',context)
