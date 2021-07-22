from django.shortcuts import render ,redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home_view(request):
	return render(request, 'home_old.html', {})

def home_depot(request):
	return render(request,'home_depot.html', {})

def home_supplier(request):
	return render(request,'home_supplier.html', {})

def login_view_home(request):
	error_message = None
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(data = request.POST)
		if form.is_valid:
			username = form.data.get('username')
			password = form.data.get('password')
			#email = form.data.get('email')
			user = authenticate(username = username, password= password)
			if user is not None:
				login(request, user)
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				else:
					return redirect(home_depot)
			else:
				error_message ="Kullanıcı adı veya şifre yanlış"

	return render(request, 'home.html', {'form':form, 'error_message':error_message})

def login_view_depot(request):
	error_message = None
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(data = request.POST)
		if form.is_valid:
			username = form.data.get('username')
			password = form.data.get('password')
			#email = form.data.get('email')
			user = authenticate(username = username, password= password)
			if user is not None:
				login(request, user)
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				else:
					return redirect(home_depot)
			else:
				error_message ="Kullanıcı adı veya şifre yanlış"

	return render(request, 'login_depot.html', {'form':form, 'error_message':error_message})


def login_view_supplier(request):
	error_message = None
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(data = request.POST)
		if form.is_valid:
			username = form.data.get('username')
			password = form.data.get('password')
			#email = form.data.get('email')
			user = authenticate(username = username, password= password)
			if user is not None:
				login(request, user)
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				else:
					return redirect(home_supplier)
			else:
				error_message ="Kullanıcı adı veya şifre yanlış"

	return render(request, 'login_supplier.html', {'form':form, 'error_message':error_message})


def logout_view(request):
	logout(request)
	return redirect('login_home')