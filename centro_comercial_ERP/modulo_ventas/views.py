from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from .models import *
import datetime 
from .models import Venta
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .forms import *
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
def consultarVentas(request):
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
def generarReporteDeVentas(request):
    return render(request, 'generarReporteDeVentas.html')  

@login_required
def consultarServicios(request):
    return render(request, 'consultarServicios.html')

@login_required
def registrarServicio(request):
    return render(request, 'registrarServicio.html')

@login_required  
def modificarEliminarServicio(request):
    return render(request, 'modificarEliminarServicio.html')

@login_required
def consultarClientes(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', 'nombre')
    
    if query:
        if filter_by == 'nombre':
            clientes = Cliente.objects.filter(nombre__icontains=query)
        elif filter_by == 'telefono':
            clientes = Cliente.objects.filter(telefono__icontains=query)
        elif filter_by == 'correo':
            clientes = Cliente.objects.filter(correo__icontains=query)
        elif filter_by == 'dui':
            clientes = Cliente.objects.filter(dui__icontains=query)
        else:
            clientes = Cliente.objects.all().order_by('id')
    else:
        clientes = Cliente.objects.all().order_by()
    
    return render(request, 'consultarClientes.html', {'clientes': clientes, 'search': query, 'filter': filter_by})


@login_required
def registrarCliente(request):
    if request.method == 'POST':
        # Procesar el formulario enviado
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo registro en la base de datos
            return redirect('consultarClientes')  # Redirige a la página de consulta de clientes
    else:
        # Mostrar el formulario vacío
        form = ClienteForm()
    return render(request, 'registrarCliente.html', {'form': form})


@login_required
def modificarEliminarCliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                return redirect('consultarClientes')
        elif 'eliminar' in request.POST:
            cliente.delete()
            return redirect('consultarClientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'modificarEliminarCliente.html', {'form': form})
    
@login_required
def menu(request):
    return render(request, 'index.html')