"""ms_b2b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, login_view_supplier, login_view_depot, logout_view, home_depot, home_supplier, login_view_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homeOld/', home_view, name = "home"),
    path('', login_view_home, name = "login_home"),
    path('loginSupplier/', login_view_supplier, name = "login_view_supplier"),
    path('loginDepot/', login_view_depot, name = "login_view_depot"),
    path('logout/', logout_view, name = "logout"),
    path('homeDepot/', home_depot, name = "home_depot"),
    path('homeSupplier/', home_supplier, name = "home_supplier"),
    path('msA101Bolge/', include('ms_a101_bolges.urls', namespace = "ms_a101_bolges")),
    path('msIhale/', include('msdepot.urls', namespace = "msdepot")),
    path('msSupplier/', include('mssupplier.urls', namespace = "mssupplier")),
    path('msOrder/', include('cart.urls', namespace = "cart")),
    path("select2/", include("django_select2.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)