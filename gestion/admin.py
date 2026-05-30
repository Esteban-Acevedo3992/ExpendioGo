from django.contrib import admin
from .models import Proveedor, Empleado, Cliente, Producto, Pedido, Encargo, Venta

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Encargo)
admin.site.register(Venta)