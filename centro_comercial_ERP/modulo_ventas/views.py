from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
import datetime 
from .models import Cliente
# Create your views here.

def registrarVenta(request):
    fecha_actual = datetime.datetime.now
    return render(request,'registrarVenta.html', {"fecha": fecha_actual,})



def consultarClientes(request):
    return render(request,'consultarClientes.html')

def registrarCliente(request):
    return render(request,'registrarCliente.html')

def gestionarCliente(request):
    return render(request,'gestionarCliente.html')


def pagina1_view(request):
    return render(request, 'templates/registrarCliente.html')