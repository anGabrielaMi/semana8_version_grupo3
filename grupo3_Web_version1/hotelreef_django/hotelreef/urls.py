from django.urls import path
from . import views

urlpatterns = [
    # Usuarios
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registrar/', views.registrar, name='registrar'),
    path('recuperar_psswd/', views.recuperar_psswd, name='recuperar_psswd'),
    path('logout/', views.logout_view, name='logout'),

    # Hoteles
    path('hoteles/', views.hoteles, name='hoteles'),
    path('hoteles/nuevo/', views.hotel_nuevo, name='hotel_nuevo'),
    path('hoteles/<int:hotel_id>/', views.hotel_detalle, name='hotel_detalle'),

    # Habitaciones
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('habitaciones/nueva/', views.habitacion_nueva, name='habitacion_nueva'),

    # Reservas
    path('reservas/', views.reservas, name='reservas'),
    path('reservas/nueva/', views.reserva_nueva, name='reserva_nueva'),
    path('reservas/<int:reserva_id>/editar/', views.reserva_editar, name='reserva_editar'),
    path('reservas/<int:reserva_id>/eliminar/', views.reserva_eliminar, name='reserva_eliminar'),

    # Reseñas
    path('resenas/', views.resenas, name='resenas'),
    path('resenas/nueva/', views.resena_nueva, name='resena_nueva'),

    # Pagos
    path('pagos/', views.pagos, name='pagos'),
    path('pagos/nuevo/', views.pago_nuevo, name='pago_nuevo'),
]