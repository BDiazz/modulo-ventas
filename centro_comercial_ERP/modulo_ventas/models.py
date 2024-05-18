from django.db import models

class Usuario(models.Model):
    rol = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    contraseña = models.CharField(max_length=200)

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    dui = models.CharField(max_length=10)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    id= models.CharField(max_length=50, primary_key=True)

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50)
    id= models.CharField(max_length=50, primary_key=True)

class Periodo(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10)  # 'dias', 'semanas', 'meses', 'anios'
    precio = models.DecimalField(max_digits=5, decimal_places=2)

class Venta(models.Model):
    fecha = models.DateField()
    id= models.CharField(max_length=50, primary_key=True)
    metodoPago = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Detalle_Venta(models.Model):
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)