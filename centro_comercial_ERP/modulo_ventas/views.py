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

def registrarServicio(request):
    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST)
        periodo_form = PeriodoForm(request.POST)
        if servicio_form.is_valid() and periodo_form.is_valid():
            servicio = servicio_form.save()  # Guardar el servicio primero
            periodo = periodo_form.cleaned_data['periodos']  # Obtener el período seleccionado
            servicio.periodo = periodo  # Asignar el período al servicio
            servicio.save()  # Guardar el servicio con el período asociado
            return redirect('consultarServicios')
    else:
        servicio_form = ServicioForm()
        periodo_form = PeriodoForm()

    return render(request, 'registrarServicio.html', {'servicioForm': servicio_form, 'periodoForm': periodo_form})


def modificarEliminarServicio(request, servicioId):
    servicio = Servicio.objects.get(id=servicioId)
    try:
        periodo = Periodo.objects.get(servicio=servicio)
    except Periodo.DoesNotExist:
        periodo = None

    if request.method == 'POST':
        servicioForm = ServicioForm(request.POST, instance=servicio)
        periodoForm = PeriodoForm(request.POST, instance=periodo)
        if servicioForm.is_valid() and periodoForm.is_valid():
            servicioForm.save()
            if periodoForm.cleaned_data['periodos'] is not None:
                periodo = periodoForm.save(commit=False)
                periodo.servicio = servicio
                periodo.save()
            return redirect('consultarServicios')
    else:
        servicioForm = ServicioForm(instance=servicio)
        periodoForm = PeriodoForm(instance=periodo)
    return render(request, 'modificarEliminarServicio.html', {'servicioForm': servicioForm, 'periodoForm': periodoForm})


def consultarServicios(request):
    filter_by = request.GET.get('filter', 'nombre')
    query = request.GET.get('search', '')

    # Obtener todos los servicios y sus períodos asociados
    servicios = Servicio.objects.all()
    if query:
        if filter_by == 'nombre':
            servicios = servicios.filter(nombre__icontains=query)
        elif filter_by == 'categoria':
            servicios = servicios.filter(categoria__icontains=query)

    # Obtener todos los tipos de período disponibles
    tipos_de_periodo = Periodo.objects.values_list('tipo', flat=True).distinct()

    return render(request, 'consultarServicios.html', {'servicios': servicios, 'search': query, 'filter': filter_by, 'tipos_de_periodo': tipos_de_periodo})

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
        clientes = Cliente.objects.all().order_by('id')
    
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