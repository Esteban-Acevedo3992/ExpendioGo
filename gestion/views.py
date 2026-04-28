from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Cliente

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
                return redirect('dashboard')
            else:
                mensaje_error = "Contraseña incorrecta."
        except Cliente.DoesNotExist:
            mensaje_error = "Usuario no encontrado."

    return render(request, 'index.html', {'error': mensaje_error})

def registro(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        numero_tel = request.POST.get('numero_tel')
        contrasena = request.POST.get('contrasena')

        # Encriptar la contraseña
        hashed_password = make_password(contrasena)

        # Crear un nuevo cliente
        cliente = Cliente(nombre_cliente=nombre_cliente, numero_tel=numero_tel, contrasena=hashed_password)
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
    if 'cliente_id' not in request.session:
        return redirect('login')
    cliente = Cliente.objects.get(cliente_id=request.session['cliente_id'])
    return render(request, 'dashboard.html', {'cliente': cliente})