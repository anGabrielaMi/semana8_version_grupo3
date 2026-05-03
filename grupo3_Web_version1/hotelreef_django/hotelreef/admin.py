from django.contrib import admin
from .models import Usuario, Hotel, Habitacion, Reserva, Resena, Pago

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'nombre', 'apellido', 'correo_electronico', 'rol')
    search_fields = ('nombre', 'apellido', 'correo_electronico')
    list_filter = ('rol',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'nombre', 'direccion', 'categoria')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('habitacion_id', 'hotel', 'tipo', 'capacidad', 'precio')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('reserva_id', 'usuario', 'habitacion', 'fecha_entrada', 'fecha_salida')

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('resena_id', 'usuario', 'hotel', 'puntuacion')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pago_id', 'reserva', 'monto')