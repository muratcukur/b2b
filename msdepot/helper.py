import plotly
#import plotly.express as px

from plotly.offline import plot
import plotly.graph_objs as go

#def bolgesel_gelen_siparis_miktari(data):
#    data = data.groupby("depot_name").sum("quantity").reset_index()

##    fig = py.bar(data, x ="depot_name", y="quantity",
#    hover_data=["depot_name", "quantity"], color = "quantity",
#    labels ={'depot_name' : 'Bölge',
            # 'quantity' : 'Sipariş Miktarı'},
#    height = 400,
#   title = "Bölgesel Geln Sipariş Miktarı")
    
#    fig.update_layout(xaxis = {"categoryorder" : "total descending"})

 #   plt_div = plotly.offline.plot(fig, output_type = "div")
#    return plt_div

def bolgesel_gelen_siparis_miktari(data):
    data = data.groupby("depot_name").sum("palet").reset_index()

    fig = go.Figure()
    bar = go.Pie(labels =data["depot_name"], values=data["palet"])

    fig.update_layout(title_text='Bölgesel Gelen Sipariş Miktarı', )

    fig.add_trace(bar)
    plt_div = plot(fig, output_type='div')

    return plt_div

def ihale_kazananlar(data):
    fig = go.Figure()
    bar = go.Bar(x =data["username"], y=data["toplam"])

    fig.update_layout(title_text='İhale Kazanan Bölgeler', xaxis={'categoryorder':'total descending'})

    fig.add_trace(bar)
    plt_div = plot(fig, output_type='div')

    return plt_div

def ms_firma_sayilari(data):
    fig = go.Figure()
    bar = go.Bar(x =data["fruit_vegetable_name_yeni"], y=data["toplam"])

    fig.update_layout(title_text='MS Tedarikçi Sayıları', xaxis={'categoryorder':'total descending'})

    fig.add_trace(bar)
    plt_div = plot(fig, output_type='div')

    return plt_div