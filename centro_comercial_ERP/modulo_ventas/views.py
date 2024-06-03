from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from .models import *
import datetime 
from .models import Venta
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def registrarVenta(request):
    clientesObtenidos = Cliente.objects.all()
    fecha_actual = datetime.datetime.now 
    return render(request,'registrarVenta.html', {"fecha": fecha_actual, "clientes": clientesObtenidos,})

@login_required
def modificarVenta(request):
    return render(request, "modificarEliminarVenta.html")

@login_required
def eliminarVenta(request, identificador):
    venta = Venta.objects.get(id=identificador)
    venta.delete()
    return redirect("/consultarVentas")

@login_required
def consultar_ventas(request):
    filtro = request.GET.get('filtro', 'todas')

    ventas = Venta.objects.all()

    if filtro == 'dia':
        ventas = ventas.filter(fecha=timezone.now().date())
    elif filtro == 'semana':
        start_week = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
        end_week = start_week + timedelta(days=6)
        ventas = ventas.filter(fecha__range=[start_week, end_week])
    elif filtro == 'mes':
        ventas = ventas.filter(fecha__month=timezone.now().month)
    elif filtro == 'anio':
        ventas = ventas.filter(fecha__year=timezone.now().year)
    elif filtro == 'todas':
        pass

    # Calcular el total de todas las ventas
    total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0.00

    return render(request, 'consultarVentas.html', {'ventas': ventas, 'total_ventas': total_ventas})

@login_required
def modificarVenta(request):
    return render(request, "modificarEliminarVenta.html")


@login_required
def generar_reporte_de_ventas(request):
    return render(request, 'generarReporteDeVentas.html')  


def consultarServicios(request):
    return render(request, 'consultarServicios.html')

def registrarServicio(request):
    return render(request, 'registrarServicio.html')
    
def modificarEliminarServicio(request):
    return render(request, 'modificarEliminarServicio.html')

def menu(request):
    return render(request, 'index.html')