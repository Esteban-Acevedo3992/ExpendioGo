from django.db import models

# 1 esta va a ser la tabla del proveedor.
class Proveedor(models.Model):
    proveedor_id = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_tel = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=100)
    empresa = models.CharField(max_length=150)
    contrasena = models.CharField(max_length=255)  # Almacena la contraseña hasheada
    
    def __str__(self):
        return f"{self.nombre_proveedor} {self.apellido} - {self.empresa}"
    
# 2 tabal Empleado
class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    nombre_empleado = models.CharField(max_length=100)
    numero_tel = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=100)
    rol = models.CharField(max_length=50)
    estatus= models.CharField(default=True)
    contrasena = models.CharField(max_length=255)  # Almacena la contraseña hasheada
    
    def __str__(self):
        return f"{self.nombre_empleado} - {self.rol}"
    
# El cliente
class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    numero_tel = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=255)  # Almacena la contraseña hasheada
    email = models.EmailField(unique=True, max_length=100)
    
    def __str__(self):
        return self.nombre_cliente