from django.shortcuts import render, redirect, get_object_or_404
from functools import wraps
from .models import Usuario, Hotel, Habitacion, Reserva, Resena, Pago


# ──────────────────────────────────────────────
#  DECORADOR DE SESIÓN
# ──────────────────────────────────────────────

def login_requerido(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper


# ──────────────────────────────────────────────
#  USUARIOS
# ──────────────────────────────────────────────

def index(request):
    return render(request, 'hotelreef/index.html')


def login_view(request):
    """GET: muestra formulario. POST: valida credenciales."""
    if request.method == 'POST':
        correo = request.POST.get('correo_electronico')
        clave = request.POST.get('contraseña')
        try:
            usuario = Usuario.objects.get(correo_electronico=correo, contrasena=clave)
            request.session['usuario_id'] = usuario.usuario_id
            request.session['usuario_nombre'] = usuario.nombre
            return redirect('index')
        except Usuario.DoesNotExist:
            return render(request, 'hotelreef/login.html', {'error': 'Correo o contraseña incorrectos'})
    return render(request, 'hotelreef/login.html')


def logout_view(request):
    """Cierra la sesión del usuario."""
    request.session.flush()
    return redirect('index')


def registrar(request):
    """GET: muestra formulario. POST: crea nuevo usuario."""
    if request.method == 'POST':
        Usuario.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            correo_electronico=request.POST.get('correo_electronico'),
            telefono=request.POST.get('telefono') or None,
            rol=request.POST.get('rol'),
            contrasena=request.POST.get('contraseña'),
        )
        return redirect('index')
    return render(request, 'hotelreef/registrar.html')


def recuperar_psswd(request):
    """Página informativa de recuperación de contraseña."""
    return render(request, 'hotelreef/recuperar_psswd.html')


# ──────────────────────────────────────────────
#  HOTELES
# ──────────────────────────────────────────────

def hoteles(request):
    """Lista todos los hoteles."""
    lista = Hotel.objects.all()
    return render(request, 'hotelreef/hoteles.html', {'hoteles': lista})


def hotel_nuevo(request):
    """GET: formulario. POST: crea hotel."""
    if request.method == 'POST':
        Hotel.objects.create(
            nombre=request.POST.get('nombre'),
            direccion=request.POST.get('direccion'),
            categoria=request.POST.get('categoria') or None,
        )
        return redirect('hoteles')
    return render(request, 'hotelreef/hotel_form.html')


def hotel_detalle(request, hotel_id):
    """Detalle de un hotel con sus habitaciones."""
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    habitaciones = Habitacion.objects.filter(hotel=hotel)
    return render(request, 'hotelreef/hotel_detalle.html', {
        'hotel': hotel,
        'habitaciones': habitaciones,
    })


# ──────────────────────────────────────────────
#  HABITACIONES
# ──────────────────────────────────────────────

def habitaciones(request):
    """Lista todas las habitaciones."""
    lista = Habitacion.objects.select_related('hotel').all()
    return render(request, 'hotelreef/habitaciones.html', {'habitaciones': lista})


def habitacion_nueva(request):
    """GET: formulario. POST: crea habitación."""
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, pk=request.POST.get('hotel_id'))
        Habitacion.objects.create(
            hotel=hotel,
            tipo=request.POST.get('tipo'),
            capacidad=request.POST.get('capacidad'),
            precio=request.POST.get('precio'),
            imagen=request.FILES.get('imagen'),  #  nueva linea para imagen
        )
        return redirect('habitaciones')
    hoteles_list = Hotel.objects.all()
    return render(request, 'hotelreef/habitacion_form.html', {'hoteles': hoteles_list})


# ──────────────────────────────────────────────
#  RESERVAS — protegidas
# ──────────────────────────────────────────────

@login_requerido
def reservas(request):
    """Lista las reservas del usuario en sesión."""
    usuario_id = request.session.get('usuario_id')
    lista = Reserva.objects.select_related('usuario', 'habitacion__hotel').filter(usuario__usuario_id=usuario_id)
    return render(request, 'hotelreef/reservas.html', {'reservas': lista})


@login_requerido
def reserva_nueva(request):
    """GET: formulario. POST: crea reserva para el usuario en sesión."""
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, pk=request.POST.get('usuario_id'))
        habitacion = get_object_or_404(Habitacion, pk=request.POST.get('habitacion_id'))
        reserva = Reserva.objects.create(
            usuario=usuario,
            habitacion=habitacion,
            fecha_entrada=request.POST.get('fecha_entrada'),
            fecha_salida=request.POST.get('fecha_salida'),
            cantidad_personas=request.POST.get('cantidad_personas'),
        )
        return redirect(f'/pagos/nuevo/?reserva_id={reserva.reserva_id}')
    habitaciones_list = Habitacion.objects.select_related('hotel').all()
    habitacion_preseleccionada = request.GET.get('habitacion_id')
    return render(request, 'hotelreef/reserva_form.html', {
        'habitaciones': habitaciones_list,
        'habitacion_preseleccionada': habitacion_preseleccionada,
    })


@login_requerido
def reserva_editar(request, reserva_id):
    """GET: formulario con datos actuales. POST: actualiza fechas y personas."""
    usuario_id = request.session.get('usuario_id')
    reserva = get_object_or_404(Reserva, pk=reserva_id, usuario__usuario_id=usuario_id)
    if request.method == 'POST':
        reserva.fecha_entrada = request.POST.get('fecha_entrada')
        reserva.fecha_salida = request.POST.get('fecha_salida')
        reserva.cantidad_personas = request.POST.get('cantidad_personas')
        reserva.save()
        return redirect('reservas')
    return render(request, 'hotelreef/reserva_editar.html', {'reserva': reserva})


@login_requerido
def reserva_eliminar(request, reserva_id):
    """POST: elimina la reserva del usuario en sesión."""
    usuario_id = request.session.get('usuario_id')
    reserva = get_object_or_404(Reserva, pk=reserva_id, usuario__usuario_id=usuario_id)
    if request.method == 'POST':
        reserva.delete()
    return redirect('reservas')


# ──────────────────────────────────────────────
#  RESEÑAS
# ──────────────────────────────────────────────

def resenas(request):
    """Lista todas las reseñas."""
    lista = Resena.objects.select_related('usuario', 'hotel').all()
    return render(request, 'hotelreef/resenas.html', {'resenas': lista})


@login_requerido
def resena_nueva(request):
    """GET: formulario. POST: crea reseña para el usuario en sesión."""
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, pk=request.POST.get('usuario_id'))
        hotel = get_object_or_404(Hotel, pk=request.POST.get('hotel_id'))
        Resena.objects.create(
            usuario=usuario,
            hotel=hotel,
            comentario=request.POST.get('comentario'),
            puntuacion=request.POST.get('puntuacion'),
        )
        return redirect('resenas')
    hoteles_list = Hotel.objects.all()
    return render(request, 'hotelreef/resena_form.html', {
        'hoteles': hoteles_list,
    })


# ──────────────────────────────────────────────
#  PAGOS — protegidas
# ──────────────────────────────────────────────

@login_requerido
def pagos(request):
    """Lista los pagos de las reservas del usuario en sesión."""
    usuario_id = request.session.get('usuario_id')
    lista = Pago.objects.select_related(
        'reserva__usuario',
        'reserva__habitacion__hotel',
    ).filter(reserva__usuario__usuario_id=usuario_id)
    return render(request, 'hotelreef/pagos.html', {'pagos': lista})


@login_requerido
def pago_nuevo(request):
    """GET: formulario. POST: crea pago con monto calculado."""
    if request.method == 'POST':
        reserva = get_object_or_404(
            Reserva.objects.select_related('habitacion'),
            pk=request.POST.get('reserva_id')
        )
        noches = (reserva.fecha_salida - reserva.fecha_entrada).days
        monto = reserva.habitacion.precio * noches
        Pago.objects.create(
            reserva=reserva,
            monto=monto,
        )
        return redirect('pagos')
    usuario_id = request.session.get('usuario_id')
    reservas_list = Reserva.objects.select_related(
        'habitacion__hotel'
    ).filter(usuario__usuario_id=usuario_id)
    reserva_preseleccionada = request.GET.get('reserva_id')
    return render(request, 'hotelreef/pago_form.html', {
        'reservas': reservas_list,
        'reserva_preseleccionada': reserva_preseleccionada,
    })