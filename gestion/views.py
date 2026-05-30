from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Cliente, Producto, Proveedor, Empleado, Pedido, Encargo, Venta

# Create your views here.
def login(request):
    mensaje_error = None
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        contrasena = request.POST.get('contrasena')

        try:
            cliente = Cliente.objects.get(nombre_cliente=nombre_cliente)
            if check_password(contrasena, cliente.contrasena):
                request.session['cliente_id'] = cliente.cliente_id

                # Redirige según tipo
                if cliente.tipo == 'admin':
                    return redirect('dashboard')
                else:
                    return redirect('catalogo')
            else:
                mensaje_error = "Contraseña incorrecta."
        except Cliente.DoesNotExist:
            mensaje_error = "Usuario no encontrado."

    return render(request, 'index.html', {'error': mensaje_error})

def solo_admin(request):
    cliente = get_cliente(request)
    if not cliente or cliente.tipo != 'admin':
        return False
    return True

def registro(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        numero_tel = request.POST.get('numero_tel')
        email = request.POST.get('email')  # Asegúrate de que el campo en tu formulario se llame 'email'
        contrasena = request.POST.get('contrasena')

        # Encriptar la contraseña
        hashed_password = make_password(contrasena)

        # Crear un nuevo cliente
        cliente = Cliente(nombre_cliente=nombre_cliente, numero_tel=numero_tel, email=email, contrasena=hashed_password, tipo='cliente')
        cliente.save()

        return redirect('login')
    return render(request, 'registro.html')

def recuperar(request):
    mensaje = None
    
    if request.method == 'POST':
        # En tu recuperar.html debes asegurarte de que el input se llame 'email'
        correo = request.POST.get('email') 
        
        try:
            # Buscamos al cliente (asumiendo que le agregaste el campo email al modelo Cliente, 
            # si no, cámbialo por numero_tel o nom_cliente según lo que uses)
            cliente = Cliente.objects.get(email=correo) 
            
            # Le asignamos una contraseña temporal y la encriptamos
            password_temporal = "Expendiogo123"
            cliente.contrasena = make_password(password_temporal)
            cliente.save()
            
            mensaje = f"Éxito. Tu contraseña temporal es: {password_temporal}"
            
        except Cliente.DoesNotExist:
            mensaje = "No existe ninguna cuenta con ese correo."
            
    return render(request, 'recuperar.html', {'mensaje': mensaje})

def dashboard(request):
    if not solo_admin(request):
        return redirect('catalogo')
    cliente = Cliente.objects.get(cliente_id=request.session['cliente_id'])
    
    # Productos bajos
    productos_bajos = Producto.objects.filter(stock__lte=10)
    cantidad_bajos = productos_bajos.count()
    
    # Pedidos pendientes
    pedidos_pendientes = Encargo.objects.filter(estatus='pendiente').count()
    
    return render(request, 'dashboard.html', {
        'cliente': cliente,
        'cantidad_bajos': cantidad_bajos,
        'pedidos_pendientes': pedidos_pendientes,
    })

def logout(request):
    request.session.flush()
    return redirect('login')

def finanzas(request):
    if not solo_admin(request):
        return redirect('catalogo')
    proveedores = Proveedor.objects.all()
    return render(request, 'finanzas.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_proveedor')
        apellido = request.POST.get('apellido')
        numero_telefonico = request.POST.get('numero_tel')
        correo_electronico = request.POST.get('email')
        direccion = request.POST.get('direccion')
        empresa = request.POST.get('empresa')

        Proveedor.objects.create(
            nombre_proveedor=nombre,
            apellido=apellido,
            numero_tel=numero_telefonico,
            email=correo_electronico,
            direccion=direccion,
            empresa=empresa
        )
        return redirect('finanzas')
    
    return redirect('finanzas') 
    
def editar_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.get(proveedor_id=proveedor_id)
    if request.method == 'POST':
        proveedor.nombre_proveedor = request.POST.get('nombre_proveedor')
        proveedor.apellido = request.POST.get('apellido')
        proveedor.numero_tel = request.POST.get('numero_tel')
        proveedor.email = request.POST.get('email')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.empresa = request.POST.get('empresa')
        proveedor.save()
        return redirect('finanzas')
    
    return redirect('finanzas') 
    
def eliminar_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.get(proveedor_id=proveedor_id)
    proveedor.delete()
    return redirect('finanzas')

def get_cliente(request):
    if 'cliente_id' not in request.session:
        return None
    return Cliente.objects.get(cliente_id=request.session['cliente_id'])

def pedidos(request):
    cliente = get_cliente(request)
    if not solo_admin(request):
        return redirect('catalogo')
    
    encargos = Encargo.objects.all().order_by('-fecha_encargo')
    
    # Encargo seleccionado al hacer click
    encargo_id = request.GET.get('encargo_id')
    encargo_seleccionado = None
    if encargo_id:
        encargo_seleccionado = Encargo.objects.get(encargo_id=encargo_id)
    
    return render(request, 'pedidos.html', {
        'cliente': cliente,
        'encargos': encargos,
        'encargo_seleccionado': encargo_seleccionado
    })

def cambiar_status_encargo(request, encargo_id):
    encargo = Encargo.objects.get(encargo_id=encargo_id)
    if request.method == 'POST':
        nuevo_status = request.POST.get('status')
        encargo.estatus = nuevo_status
        encargo.save()
    return redirect(f'/pedidos/?encargo_id={encargo_id}')

def inventario(request):
    if not solo_admin(request):
        return redirect('catalogo')
    productos = Producto.objects.all()  # jala todos los productos de la BD
    proveedores = Proveedor.objects.all()
    return render(request, 'inventario.html', {'productos': productos, 'proveedores': proveedores})

def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_producto')
        categoria = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        proveedor_id = request.POST.get('proveedor')
        proveedor = Proveedor.objects.get(proveedor_id=proveedor_id)

        Producto.objects.create(
            nombre_producto=nombre,
            categoria=categoria,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            proveedor=proveedor
        )
        return redirect('inventario')
    
def editar_producto(request, producto_id):
    producto = Producto.objects.get(producto_id=producto_id)
    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.categoria = request.POST.get('categoria')
        producto.precio_compra = request.POST.get('precio_compra')
        producto.precio_venta = request.POST.get('precio_venta')
        producto.stock = request.POST.get('stock')
        proveedor_id = request.POST.get('proveedor')
        producto.proveedor = Proveedor.objects.get(proveedor_id=proveedor_id)
        producto.save()
        return redirect('inventario')
    
    return redirect('inventario')

def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(producto_id=producto_id)
    producto.delete()
    return redirect('inventario')

def configuracion(request):
    if not solo_admin(request):
        return redirect('catalogo')
    return render(request, 'configuracion.html')

def catalogo(request):
    cliente = get_cliente(request)
    if not cliente:
        return redirect('login')
    
    productos = Producto.objects.all()
    categorias = Producto.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'catalogo.html', {
        'cliente': cliente,
        'productos': productos,
        'categorias': categorias,
    })

def agregar_encargo(request):
    cliente = get_cliente(request)
    if not cliente:
        return redirect('login')
    
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad'))
        producto = Producto.objects.get(producto_id=producto_id)
        total = producto.precio_venta * cantidad
        
        Encargo.objects.create(
            cliente=cliente,
            producto=producto,
            cantidad=cantidad,
            total_venta=total
        )
        return redirect('catalogo')
    
def mis_encargos(request):
    cliente = get_cliente(request)
    if not cliente:
        return redirect('login')
    
    encargos = Encargo.objects.filter(cliente=cliente).order_by('-fecha_encargo')
    
    return render(request, 'mis_encargos.html', {
        'cliente': cliente,
        'encargos': encargos,
    })

def cancelar_encargo(request, encargo_id):
    cliente = get_cliente(request)
    if not cliente:
        return redirect('login')
    encargo = Encargo.objects.get(encargo_id=encargo_id, cliente=cliente)
    encargo.estatus = 'cancelado'
    encargo.save()
    return redirect('mis_encargos')