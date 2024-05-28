from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
import datetime 
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def registrarVenta(request):
    fecha_actual = datetime.datetime.now 
    return render(request,'registrarVenta.html', {"fecha": fecha_actual,})

@login_required
def consultar_ventas(request):
    return render(request, 'consultarVentas.html')   

   
@login_required
def generar_reporte_de_ventas(request):
    return render(request, 'generarReporteDeVentas.html')  