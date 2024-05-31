from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from .models import *
import datetime 
# Create your views here.

def registrarVenta(request):
    clientesObtenidos = Cliente.objects.all()
    fecha_actual = datetime.datetime.now
    return render(request,'registrarVenta.html', {"fecha": fecha_actual, "clientes": clientesObtenidos,})

def modificarVenta(request):
    return render(request, "modificarEliminarVenta.html")

def eliminarVenta(request, identificador):
    venta = Venta.objects.get(id=identificador)
    venta.delete()
    return redirect("/consultarVentas")