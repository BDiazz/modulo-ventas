from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
import datetime 
# Create your views here.

def registrarVenta(request):
    fecha_actual = datetime.datetime.now
    return render(request,'registrarVenta.html', {"fecha": fecha_actual,})