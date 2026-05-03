from django.db import models


class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre = models.TextField()
    apellido = models.TextField()
    correo_electronico = models.TextField(unique=True)
    telefono = models.TextField(blank=True, null=True)
    rol = models.TextField()
    contrasena = models.TextField(db_column='contraseña')

    class Meta:
        db_table = 'Usuario'
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    nombre = models.TextField()
    direccion = models.TextField()
    categoria = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Hotel'
        managed = False

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    habitacion_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, db_column='hotel_id')
    tipo = models.TextField()
    capacidad = models.IntegerField()
    precio = models.FloatField()
    imagen = models.ImageField(upload_to='habitaciones/', blank=True, null=True)  # nueva linea para img

    class Meta:
        db_table = 'Habitacion'
        managed = False

    def __str__(self):
        return f"{self.tipo} - Hotel {self.hotel_id}"


class Reserva(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, db_column='habitacion_id')
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    cantidad_personas = models.IntegerField()

    class Meta:
        db_table = 'Reserva'
        managed = False

    def __str__(self):
        return f"Reserva {self.reserva_id} - {self.usuario}"


class Resena(models.Model):
    resena_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, db_column='hotel_id')
    comentario = models.TextField()
    puntuacion = models.IntegerField()

    class Meta:
        db_table = 'Resena'
        managed = False

    def __str__(self):
        return f"Reseña de {self.usuario} - {self.puntuacion}/5"


class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, db_column='reserva_id')
    monto = models.IntegerField()

    class Meta:
        db_table = 'Pago'
        managed = False

    def __str__(self):
        return f"Pago {self.pago_id} - ${self.monto}"