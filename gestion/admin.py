from django.contrib import admin
from .models import Proveedor, Empleado, Cliente

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Empleado)
admin.site.register(Cliente)