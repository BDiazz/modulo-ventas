from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
import datetime 
# Create your views here.

def registrarVenta(request):
    fecha_actual = datetime.datetime.now
    return render(request,'registrarVenta.html', {"fecha": fecha_actual,})
def consultarServicios(request):
    return render(request, 'consultarServicios.html')
def regristarServicio(request):
    return render(request, 'registrarServicio.html')
def modificarEliminarServicio(request):
    return render(request, 'modificarEliminarServicio.html')

