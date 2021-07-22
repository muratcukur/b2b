from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IhaleForm, IhaleTeklifForm, SearchFruitVegetableForm, TedarikciAnketForm, IhaleIkinciTurForm, IhaleIkinciTurTeklifForm, BaglantiliUrunIhaleForm, BaglantiliIhaleTeklifForm
from cart.forms import OrderForm
from .models import IhaleYeni, IhaleTeklif, RakipFiyatTakip, TedarikciAnket, IhaleIkinciTur, IhaleIkinciTurTeklif, BaglantiliUrunIhalesi, BaglantiliIhaleAyHedefTonaj, BaglantiliIhaleTeklif
from mssupplier.models import SupplierStock
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
import json
from ms_a101_bolges.models import DepotOrder
from .helper import bolgesel_gelen_siparis_miktari, ihale_kazananlar, ms_firma_sayilari
import pandas as pd
from django.db import connection
from msdepot.models import MeyveSebzeYeni

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from django.contrib.staticfiles.storage import staticfiles_storage
# Create your views here.


@login_required
def upload_ihale_view(request):
    success_message = None
    error_message = None
    form = IhaleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit = False)
        obj.user_name = request.user
        obj.save()

        form = IhaleForm()

    context = {
    'form' : form,
    'success_message' : success_message,
    'error_message' : error_message,
    }

    return render(request, 'msdepot/uploadIhale.html',context)

@login_required
def ihale_view(request):
    success_message = None
    error_message = None
    supplier_fruit_vegetable = None
    today = date.today()

    if request.user.is_superuser:
        ihales = IhaleYeni.objects.all()
    else:
        supplier_fruit_vegetable = SupplierStock.objects.filter(supplier_name = request.user).order_by("fruit_vegetable_name").values('fruit_vegetable_name').distinct()

        ihales = IhaleYeni.objects.filter(fruit_vegetable_name__in = supplier_fruit_vegetable).all()
    
    context = {
    'ihales' : ihales,
    'today' : today,
    'supplier_fruit_vegetable' : supplier_fruit_vegetable,
    }

    return render(request, 'msdepot/viewIhale.html',context)

@login_required
def detail_ihale_view(request, pk):
    today = date.today()
    detail_ihale = None
    detail_ihale_teklif = None
    error_message = None

    ihale_teklif_form = IhaleTeklifForm(request.POST or None, request.FILES or None)
    ihale_ikinci_tur_form = IhaleIkinciTurForm(request.POST or None, request.FILES or None)
    ihale_id = int(pk)

    try:
        detail_ihale = IhaleYeni.objects.get(id = ihale_id)
        detail_ihale_teklif = IhaleTeklif.objects.all().filter(ihale_id = ihale_id).order_by('fiyat')
    except:
        IhaleYeni.DoesNotExist
        return redirect('msdepot:ihale_view')
    
    if request.method == "POST":
        if "ihale_teklif_sub" in request.POST:
            ihale_teklif_form = IhaleTeklifForm(data=request.POST, files=request.FILES)
            if ihale_teklif_form.is_valid():
                obj = ihale_teklif_form.save(commit = False)
                obj.tedarikci = request.user
                obj.ihale_id = IhaleYeni.objects.get(id = ihale_id)
                obj.save()

        elif 'ikinci_tur_sub' in request.POST:
            ihale_ikinci_tur_form = IhaleIkinciTurForm(data=request.POST, files=request.FILES)
            if ihale_ikinci_tur_form.is_valid():
                num_results = IhaleIkinciTur.objects.filter(ihale_id = ihale_id).count()
                if num_results >=1:
                    error_message = "Bu ihale için 2. tur zaten mevcut"
                else:
                    obj = ihale_ikinci_tur_form.save(commit = False)
                    obj.ihale_id = IhaleYeni.objects.get(id = ihale_id)
                    obj.save()
                    ihale_ikinci_tur_form.save_m2m()

    context = {
    'detail_ihale' : detail_ihale,
    'detail_ihale_teklif': detail_ihale_teklif,
    'today' : today,
    'ihale_teklif_form':ihale_teklif_form,
    'ihale_ikinci_tur_form':ihale_ikinci_tur_form,
    'error_message':error_message,
    }

    return render(request, 'msdepot/viewIhaleDetail.html',context)


@login_required
def stock_view(request):
    success_message = None
    error_message = None
    search_stocks= None
    response_data = {}
   
    stocks = SupplierStock.objects.all()
    unique_fruit_vegetable = SupplierStock.objects.order_by("fruit_vegetable_name").values('fruit_vegetable_name').distinct()

    form = OrderForm(request.POST or None, request.FILES or None)
    form_search = SearchFruitVegetableForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if 'order_sub' in request.POST or request.is_ajax():
            form = OrderForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.supplier = request.POST.get('supplier_name')
                obj.product = request.POST.get('fruit_vegetable')
                obj.save()

            response_data["message"] = "successview"
         

            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else:
            form = OrderForm()        

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

    return render(request, 'msdepot/viewStock.html',context)

@login_required
def dashboard_view(request):

    # BÖLGELERDEN GELEN SİPARİŞ MİKTARI GRAFİĞİ
    df = pd.DataFrame(DepotOrder.objects.all().values())
    graph_bolgesel_gelen_siparis = bolgesel_gelen_siparis_miktari(df)
    
    # EN FAZLA İHALE KAZANAN FİRMALARIN GRAFİĞİ
    cursor = connection.cursor()
    query = """ WITH data as(select tedarikci_id, count(*) as toplam  from (select ihale_id_id, tedarikci_id,fiyat, rank() over(PARTITION BY ihale_id_id ORDER BY fiyat desc ) as min_ihale from msdepot_ihaleteklif) as sub where min_ihale == 1 GROUP BY tedarikci_id) select a.tedarikci_id, a.toplam, b.username from data as a left join auth_user b on a.tedarikci_id = b.id """
    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.description
    column = []
    for col in columns:
        column.append(col[0])
    ihale_kazanan = pd.DataFrame(result,columns=column)
    graph_ihale_kazananlar = ihale_kazananlar(ihale_kazanan)

    #MEYVE SEBZEYİ KAÇ FİRMANIN SATTIĞINI GÖSTEREN GRAFİK
    query2 = """  WITH data as (select fruit_vegetable_name_id, count(*) as toplam from mssupplier_supplierstock GROUP by fruit_vegetable_name_id) SELECT b.fruit_vegetable_name, a.toplam from data as a left join msdepot_meyvesebzeyeni as b on a.fruit_vegetable_name_id = b.id """
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = cursor.description
    cursor.close()
    column = []
    for col in columns:
        column.append(col[0])
    ms_firma_sayisi = pd.DataFrame(result,columns=column)
    graph_ms_firma_sayilari = ms_firma_sayilari(ms_firma_sayisi)


    context = {
    'graph_bolgesel_gelen_siparis' : graph_bolgesel_gelen_siparis,
    'graph_ihale_kazananlar' : graph_ihale_kazananlar,
    'graph_ms_firma_sayilari' : graph_ms_firma_sayilari,
    }

    return render(request, 'msdepot/viewDashboard.html', context)

@login_required
def scrap(request):
    #https://dev.to/mdrhmn/web-scraping-using-django-and-selenium-3ecg
    data_migros = None
    data_şok = None

    rakipFiyatTakip = RakipFiyatTakip.objects.all()

    fruits = ["elma starking", "elma golden", "elma granny", "muz yerli", "kıvırcık", "erik angelica", "erik papaz", "patates", "soğan"]

    if request.method == "POST":

        RakipFiyatTakip.objects.all().delete()  ## Entry being Model Name. 

        meyve_fiyat_migros = {}
        meyve_fiyat_migros['Fiyat'] = {}
        meyve_fiyat_migros['İndirimde mi?'] = {}

        for fruit in fruits:
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1080")
            url = staticfiles_storage.path('chromedriver.exe')
            driver = webdriver.Chrome(url, options=options)
            driver.get("https://www.migros.com.tr/")
            time.sleep(3)
            try: 
                popup = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "mfp-close")))
                popup.click()
            except:
                pass
            
            try: 
                popup = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "fa-w-10")))
                popup.click()
            except:
                pass
            search_bar = driver.find_element_by_xpath('//*[@id="product-search-combobox--trigger"]')
            search_bar.clear()
            search_bar.send_keys(fruit)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(2)
            isim = driver.find_element_by_class_name('product-name').text
            try:
                elements=WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.product-cards > .ng-star-inserted')))
                old_fiyat = elements[0].find_element_by_css_selector(".price-old .amount").text
                new_fiyat = elements[0].find_element_by_css_selector(".price-new .amount").text
                fiyat = old_fiyat + " "+ new_fiyat
                meyve_fiyat_migros['Fiyat'][isim] = fiyat
                meyve_fiyat_migros['İndirimde mi?'][isim] = "evet"
            except:
                fiyat = driver.find_element_by_class_name('amount').text
                meyve_fiyat_migros['Fiyat'][isim] = fiyat
                meyve_fiyat_migros['İndirimde mi?'][isim] = "hayır"

            driver.close()

        #data_migros = pd.DataFrame(list(meyve_fiyat_migros.items()), columns=['Meyve Sebze', 'Fiyat'])

        data_migros = pd.DataFrame(meyve_fiyat_migros).reset_index()
        data_migros = data_migros.rename(columns={'index': 'Meyve Sebze'})

        data_migros["Mağaza"] = "Migros"      

        df_records_migros = data_migros.to_dict('records')

        model_instances = [RakipFiyatTakip(
            fruit_vegetable_name=record['Meyve Sebze'],
            price=record['Fiyat'],
            rakip=record['Mağaza'],
            indirim=record['İndirimde mi?'],
        ) for record in df_records_migros]

        RakipFiyatTakip.objects.bulk_create(model_instances)

        #data_migros = data_migros.to_html()

        meyve_fiyat_şok = {}
        meyve_fiyat_şok['Fiyat'] = {}
        meyve_fiyat_şok['İndirimde mi?'] = {}

        for fruit in fruits:
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1080")
            url = staticfiles_storage.path('chromedriver.exe')
            driver = webdriver.Chrome(url, options=options)
            driver.get("https://www.sokmarket.com.tr/")
            search_bar = driver.find_element_by_name('search')
            search_bar.clear()
            search_bar.send_keys(fruit)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(2)
            parentDiv = driver.find_elements_by_class_name("list-item")
            try:
                if parentDiv[0].find_element_by_css_selector(".pricetag .old").text:
                    isim = parentDiv[0].find_element_by_class_name("content-title").text
                    fiyat = parentDiv[0].find_element_by_class_name("pricetag").text
                    meyve_fiyat_şok['Fiyat'][isim] = fiyat
                    meyve_fiyat_şok['İndirimde mi?'][isim] = "evet"
                    driver.close()
                else:
                    meyve_fiyat_şok['Fiyat'][isim] = fiyat
                    meyve_fiyat_şok['İndirimde mi?'][isim] = "hayır"
                    driver.close()
            except:
                driver.close()

        #data_şok = pd.DataFrame(list(meyve_fiyat_şok.items()), columns=['Meyve Sebze', 'Fiyat'])

        data_şok = pd.DataFrame(meyve_fiyat_şok).reset_index()
        data_şok = data_şok.rename(columns={'index': 'Meyve Sebze'})

        data_şok["Mağaza"] = "Şok"
        
        df_records_şok = data_şok.to_dict('records')

        model_instances = [RakipFiyatTakip(
            fruit_vegetable_name=record['Meyve Sebze'],
            price=record['Fiyat'],
            rakip=record['Mağaza'],
            indirim=record['İndirimde mi?'],
        ) for record in df_records_şok]

        RakipFiyatTakip.objects.bulk_create(model_instances)

        rakipFiyatTakip = RakipFiyatTakip.objects.all()

        #data_şok = data_şok.to_html()

    context = {
        #'data_migros' : data_migros,
        #'data_şok' : data_şok,
        'rakipFiyatTakip' : rakipFiyatTakip,
    }

    return render(request, 'msdepot/viewRakipFiyat.html', context)

def upload_anket_view(request):
    success_message = None
    error_message = None
    form = TedarikciAnketForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit = False)
        obj.kullanici = request.user
        obj.save()

        form = TedarikciAnketForm()

    context = {
    'form' : form,
    'success_message' : success_message,
    'error_message' : error_message,
    }

    return render(request, 'msdepot/uploadAnket.html',context)

def list_anket_view(request):
    success_message = None
    error_message = None

    ankets = TedarikciAnket.objects.all()
    
    context = {
    'ankets' : ankets,  
    }

    return render(request, 'msdepot/viewAnket.html',context)

def list_ikinci_tur_view(request):

    ikinci_turs = IhaleIkinciTur.objects.all()

    context = {
    'ikinci_turs' : ikinci_turs, 
    }

    return render(request, 'msdepot/viewSecondTour.html',context)


@login_required
def detail_ihale_second_tour_view(request, pk):
    today = date.today()
    detail_ihale = None
    detail_ihale_teklif = None
    error_message = None

    ihale_id = int(pk)

    ihale_ikinci_tur_teklif_form = IhaleIkinciTurTeklifForm(request.POST or None, request.FILES or None)

    if IhaleIkinciTur.objects.filter(ihale_id = ihale_id, suppliers__in = [request.user]) or 'MeyveSebzeDeposu' in request.user.username:

        try:
            detail_ihale_ikinci_tour = IhaleYeni.objects.get(id = ihale_id)
            detail_ihale_ikinci_tour_teklif = IhaleIkinciTur.objects.get(ihale_id = ihale_id)
            detail_ihale_ikinci_tour_teklifler = IhaleIkinciTurTeklif.objects.all().filter(ihale_id = ihale_id).order_by('fiyat')
                
        except:
            IhaleYeni.DoesNotExist
            return redirect('msdepot:list_ikinci_tur_view')

        if request.method == "POST":
                if "ihale_teklif_sub" in request.POST:
                    ihale_teklif_form = IhaleIkinciTurTeklifForm(data=request.POST, files=request.FILES)
                    if ihale_teklif_form.is_valid():
                        obj = ihale_teklif_form.save(commit = False)
                        obj.tedarikci = request.user
                        obj.ihale_id = IhaleYeni.objects.get(id = ihale_id)
                        obj.save()

        context = {
        'today' : today,
        'detail_ihale_ikinci_tour' : detail_ihale_ikinci_tour,
        'detail_ihale_ikinci_tour_teklif':detail_ihale_ikinci_tour_teklif,
        'ihale_ikinci_tur_teklif_form':ihale_ikinci_tur_teklif_form,
        'detail_ihale_ikinci_tour_teklifler':detail_ihale_ikinci_tour_teklifler,
        }
        return render(request, 'msdepot/viewIhaleIkınciTourDetail.html',context)

    else:
        error_message = "Bu ihalenin 2. turunu görüntüleme yetkiniz yoktur."
        context = {
            'error_message':error_message
        }
    
        return render(request, 'msdepot/viewIhaleIkınciTourDetail.html',context)

def list_ikinci_tur_supplier_based_view(request):

    ikinci_turs = IhaleIkinciTur.objects.filter(suppliers__in = [request.user])

    context = {
    'ikinci_turs' : ikinci_turs, 
    }

    return render(request, 'msdepot/viewSecondTour.html',context)


@login_required
def upload_baglantili_ihale_view(request):
    success_message = None
    error_message = None
    counter = None

    form = BaglantiliUrunIhaleForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user_name = request.user
            obj.save()


            ay_hedef_tonaj = {}
            ay_hedef_tonaj['baglantiliihaleid'] = {}
            ay_hedef_tonaj['month'] = {}
            ay_hedef_tonaj['planlanan_hedef_fiyat'] = {}
            ay_hedef_tonaj['planlanan_hedef_tonaj'] = {}

            
            #for i in range(1, 24):  # zaten 1 yılda 12 ay olduğu için 2 ile başlıyor id ler 14 e kadar gidince tüm ayları kapsar. Ama silme işlemi yapıldığında 24 e kadar gidebilir.
            counter = request.POST["counter"]
            for i in range(1, int(counter)+1):  # counter sayısını html de her yeni ihale eklendiğinde artırıyorum.
                try:
                    if request.POST["month"+str(i)] != None :
                        ay_hedef_tonaj["baglantiliihaleid"][str(i)] = BaglantiliUrunIhalesi.objects.get(id=obj.id)                   
                        ay_hedef_tonaj["month"][str(i)] = request.POST["month"+str(i)]
                        ay_hedef_tonaj["planlanan_hedef_fiyat"][str(i)] = request.POST["hedef_fiyat"+str(i)]
                        ay_hedef_tonaj["planlanan_hedef_tonaj"][str(i)] = request.POST["hedef_tonaj"+str(i)]
                    
                except:
                    pass

            data_ay_hedef_tonaj = pd.DataFrame(ay_hedef_tonaj).reset_index()

            df_records_ay_hedef_tonaj = data_ay_hedef_tonaj.to_dict('records')

            model_instances = [BaglantiliIhaleAyHedefTonaj(
                baglantiliihaleid=record['baglantiliihaleid'],
                month=record['month'],
                planlanan_hedef_fiyat=record['planlanan_hedef_fiyat'],
                planlanan_hedef_tonaj=record['planlanan_hedef_tonaj'],
            ) for record in df_records_ay_hedef_tonaj]

            BaglantiliIhaleAyHedefTonaj.objects.bulk_create(model_instances)

            form = BaglantiliUrunIhaleForm()
    
    context = {
    'form' : form,
    'success_message' : success_message,
    'error_message' : error_message,
    'counter' : counter,

    }

    return render(request, 'msdepot/uploadBaglantiliUrunIhale.html',context)



@login_required
def baglantili_ihale_view(request):
    success_message = None
    error_message = None
    supplier_fruit_vegetable = None
    today = date.today()

    if request.user.is_superuser:
        ihales = BaglantiliUrunIhalesi.objects.all()
        ay_hedef_tonaj = BaglantiliIhaleAyHedefTonaj.objects.all()
    else:
        supplier_fruit_vegetable = SupplierStock.objects.filter(supplier_name = request.user).order_by("fruit_vegetable_name").values('fruit_vegetable_name').distinct()

        ihales = BaglantiliUrunIhalesi.objects.filter(fruit_vegetable_name__in = supplier_fruit_vegetable).all()

        ihale_ids = ihales.values('id').distinct()

        ay_hedef_tonaj = BaglantiliIhaleAyHedefTonaj.objects.filter(baglantiliihaleid__in = ihale_ids)
    
    context = {
    'ihales' : ihales,
    'ay_hedef_tonaj' : ay_hedef_tonaj,
    'today' : today,
    'supplier_fruit_vegetable' : supplier_fruit_vegetable,
    }

    return render(request, 'msdepot/viewBaglantiliIhale.html',context)


@login_required
def detail_baglantili_ihale_view(request, pk):
    today = date.today()
    detail_ihale = None
    ay_hedef_tonaj = None
    error_message = None

    baglantili_ihale_teklif_form = BaglantiliIhaleTeklifForm(request.POST or None, request.FILES or None)
    ihale_id = int(pk)

    detail_ihale_teklif = BaglantiliIhaleTeklif.objects.all().filter(baglantiliihaleid = ihale_id).order_by('tedarikci')

    try:
        detail_ihale = BaglantiliUrunIhalesi.objects.get(id = ihale_id)
        ay_hedef_tonaj_table = BaglantiliIhaleAyHedefTonaj.objects.filter(baglantiliihaleid = ihale_id)
    except:
        BaglantiliUrunIhalesi.DoesNotExist
        return redirect('msdepot:baglantili_ihale_view')
    
    if request.method == "POST":
        if "ihale_teklif_sub" in request.POST:

            ay_hedef_tonaj = {}
            ay_hedef_tonaj['baglantiliihaleid'] = {}
            ay_hedef_tonaj['tedarikci'] = {}
            ay_hedef_tonaj['month'] = {}
            ay_hedef_tonaj['planlanan_hedef_tonaj'] = {}
            ay_hedef_tonaj['planlanan_hedef_fiyat'] = {}

            #for i in range(1, 24):  # zaten 1 yılda 12 ay olduğu için 2 ile başlıyor id ler 14 e kadar gidince tüm ayları kapsar. Ama silme işlemi yapıldığında 24 e kadar gidebilir.
            counter = request.POST["counter"]
            for i in range(1, int(counter)+1):  # counter sayısını html de her yeni ihale eklendiğinde artırıyorum.
                try:
                    if request.POST["month"+str(i)] != None :
                        ay_hedef_tonaj["baglantiliihaleid"][str(i)] = BaglantiliUrunIhalesi.objects.get(id=ihale_id)
                        ay_hedef_tonaj['tedarikci'][str(i)] = request.user      
                        ay_hedef_tonaj["month"][str(i)] = request.POST["month"+str(i)]
                        ay_hedef_tonaj["planlanan_hedef_tonaj"][str(i)] = request.POST["hedef_tonaj"+str(i)]
                        ay_hedef_tonaj["planlanan_hedef_fiyat"][str(i)] = request.POST["hedef_fiyat"+str(i)]
                    
                except:
                    pass

            data_ay_hedef_tonaj = pd.DataFrame(ay_hedef_tonaj).reset_index()

            df_records_ay_hedef_tonaj = data_ay_hedef_tonaj.to_dict('records')

            model_instances = [BaglantiliIhaleTeklif(
                baglantiliihaleid=record['baglantiliihaleid'],
                tedarikci=record['tedarikci'],
                month=record['month'],
                planlanan_hedef_tonaj=record['planlanan_hedef_tonaj'],
                planlanan_hedef_fiyat=record['planlanan_hedef_fiyat'],
            ) for record in df_records_ay_hedef_tonaj]

            BaglantiliIhaleTeklif.objects.bulk_create(model_instances)


    context = {
    'detail_ihale' : detail_ihale,
    'ay_hedef_tonaj' : ay_hedef_tonaj_table,
    'baglantili_ihale_teklif_form' : baglantili_ihale_teklif_form,
    'detail_ihale_teklif' : detail_ihale_teklif,
    'today' : today,
    'error_message':error_message,
    }

    return render(request, 'msdepot/viewBaglantiliIhaleDetail.html',context)