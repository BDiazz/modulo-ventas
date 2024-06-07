# populate_db.py

import os
import django
import random
from datetime import date

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centro_comercial_ERP.settings')
django.setup()

from modulo_ventas.models import Usuario, Cliente, Servicio, Periodo, Venta, Detalle_Venta

# Crear usuarios
usuarios = [
    {"rol": "admin", "nombre": "Admin User", "contraseña": "admin123"},
    {"rol": "vendedor", "nombre": "Vendedor User", "contraseña": "vendedor123"},
]

for usuario_data in usuarios:
    Usuario.objects.create(**usuario_data)

# Crear clientes
clientes = [
    {"nombre": "José Jimenez", "dui": "12345678-9", "telefono": "555-1234", "correo": "jose@example.com", "direccion": "Calle 123"},
    {"nombre": "Maria Lopez", "dui": "98765432-1", "telefono": "555-5678", "correo": "maria@example.com", "direccion": "Avenida 456"},
]

for cliente_data in clientes:
    Cliente.objects.create(**cliente_data)

# Crear servicios
servicios = [
    {"nombre": "Seguridad", "descripcion": "Servicio de seguridad 24/7", "categoria": "Seguridad"},
    {"nombre": "Limpieza", "descripcion": "Servicio de limpieza diaria", "categoria": "Limpieza"},
]

for servicio_data in servicios:
    Servicio.objects.create(**servicio_data)

# Crear periodos
periodos = [
    {"servicio_id": 1, "tipo": "meses", "precio": 200.00},
    {"servicio_id": 2, "tipo": "meses", "precio": 150.00},
]

for periodo_data in periodos:
    Periodo.objects.create(**periodo_data)

# Crear ventas
ventas = [
    {"fecha": date(2024, 3, 12), "metodoPago": "efectivo", "total": 226.00, "usuario_id": 1, "cliente_id": 1},
    {"fecha": date(2024, 3, 15), "metodoPago": "tarjeta-credito", "total": 169.50, "usuario_id": 2, "cliente_id": 2},
]

for venta_data in ventas:
    Venta.objects.create(**venta_data)

# Crear detalles de venta
detalle_ventas = [
    {"cantidad": 1, "subtotal": 200.00, "servicio_id": 1, "venta_id": 1},
    {"cantidad": 1, "subtotal": 26.00, "servicio_id": 1, "venta_id": 1},
    {"cantidad": 1, "subtotal": 150.00, "servicio_id": 2, "venta_id": 2},
    {"cantidad": 1, "subtotal": 19.50, "servicio_id": 2, "venta_id": 2},
]

for detalle_venta_data in detalle_ventas:
    Detalle_Venta.objects.create(**detalle_venta_data)

print("Base de datos poblada con éxito.")
