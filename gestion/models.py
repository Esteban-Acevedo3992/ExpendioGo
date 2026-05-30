from django.db import models

# 1 esta va a ser la tabla del proveedor.
class Proveedor(models.Model):
    proveedor_id = models.AutoField(primary_key=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    nombre_proveedor = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_tel = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=100)
    direccion = models.CharField(max_length=255)
    empresa = models.CharField(max_length=150)
   
    
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
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='cliente')
    
    def __str__(self):
        return self.nombre_cliente

# La tabla de productos
class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)
    nombre_producto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_producto
    
#tabla de pedidos a proveedor
class Pedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    costo_adquisicion = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Pedido {self.pedido_id} - {self.producto.nombre_producto} x {self.cantidad}"
    
#tabla de encargos de clientes
class Encargo(models.Model):
        
    encargo_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_encargo = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
       ]
    estatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    
    def __str__(self):
        return f"Encargo {self.encargo_id} - {self.producto.nombre_producto} x {self.cantidad}"
    
#ventas del dia
class Venta(models.Model):
    venta_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Venta {self.venta_id} - {self.producto.nombre_producto} x {self.cantidad}"