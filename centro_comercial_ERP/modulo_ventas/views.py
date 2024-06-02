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
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
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

def modificarVenta(request):
    return render(request, "modificarEliminarVenta.html")


   

def generar_reporte_de_ventas(request):
    return render(request, 'generarReporteDeVentas.html')  

def vista_inicio_sesion(request):
    class FormularioInicioSesion(forms.Form):
        nombre = forms.CharField(label="Nombre de usuario")
        contraseña = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    if request.method == 'POST':
        formulario = FormularioInicioSesion(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            contraseña = formulario.cleaned_data['contraseña']
            usuario = authenticate(request, username=nombre, password=contraseña)
            if usuario is not None:
                # Autenticación exitosa
                # Guardar el usuario en la sesión
                request.session['usuario_id'] = usuario.id
                return redirect('consultar_ventas')
            else:
                # Autenticación fallida
                mensaje_error = "Nombre de usuario o contraseña incorrectos."
        else:
            # Formulario no válido
            mensaje_error = "Formulario inválido. Por favor, verifica los datos."
    else:
        formulario = FormularioInicioSesion()
        mensaje_error = None
    return render(request, 'inicio_sesion.html', {'formulario': formulario, 'mensaje_error': mensaje_error})