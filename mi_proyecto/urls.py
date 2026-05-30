"""
URL configuration for mi_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('finanzas/', views.finanzas, name='finanzas'),
    path('finanzas/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('finanzas/editar/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('finanzas/eliminar/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/status/<int:encargo_id>/', views.cambiar_status_encargo, name='cambiar_status_encargo'),
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('configuracion/', views.configuracion, name='configuracion'),

    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/agregar_encargo/', views.agregar_encargo, name='agregar_encargo'),
    path('mis_encargos/', views.mis_encargos, name='mis_encargos'),
    path('mis_encargos/cancelar/<int:encargo_id>/', views.cancelar_encargo, name='cancelar_encargo'),
]