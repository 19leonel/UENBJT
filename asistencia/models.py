from django.db import models
from django.conf import settings
from UserProfile.models import User
from datetime import datetime

# Create your models here.

dias = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miercoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
}


class Horarios(models.Model):
    """Model definition for Horario."""

    # TODO: Define fields here
    id_user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE)
    Dia = models.CharField('Dias', max_length=50, choices=dias)
    Hora_E = models.TimeField('Hora de Entrada')
    Hora_S = models.TimeField('Hora de Salida')

    class Meta:
        """Meta definition for Horario."""

        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    # def __str__(self):
    #     """Unicode representation of Horario."""
    #     pass

    @staticmethod
    def get_dias_disponible(id):
        dia_r = Horarios.objects.filter(
            id_user=id).values_list('Dia', flat=True)
        dia_d = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
        return [dia for dia in dia_d if dia not in dia_r]


class Fecha(models.Model):
    """Model definition for Fechas."""

    # TODO: Define fields here
    fecha = models.DateField('Fecha')

    class Meta:
        """Meta definition for Fechas."""

        verbose_name = 'Fecha'
        verbose_name_plural = 'Fechas'

    def __str__(self):
        """Unicode representation of Fechas."""
        r = f'{self.fecha}'
        return r


class Periodo(models.Model):
    """Model definition for Periodo."""

    periodos = models.CharField('Periodo', max_length=50, unique=True)

    class Meta:
        """Meta definition for Periodo."""

        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'

    def __str__(self):
        """Unicode representation of Periodo."""
        return self.periodos


class assistance(models.Model):
    """Model definition for Horario."""

    # TODO: Define fields here
    id_User = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE)
    id_fecha = models.ForeignKey(Fecha, verbose_name='Fecha', on_delete=models.CASCADE)
    hora_inicio = models.TimeField('Hora de Inicio', null=True, blank=True)  # ✅ CAMBIO AQUÍ
    hora_salida = models.TimeField('Hora de Salida', null=True, blank=True)
    Asis = models.BooleanField('Asistente', default=False)
    id_periodo = models.ForeignKey(Periodo,verbose_name='Periodo', on_delete=models.CASCADE)

    # def get_H_I(self):
    #     return self.hora_inicio.strftime('%H:%M')

    class Meta:
        verbose_name = 'asistencia'
        verbose_name_plural = 'asistencias'
        unique_together = ('id_User', 'id_fecha')

    def __str__(self):
        texto = f'Nombre: {self.id_User.nombre} -- cedula: {self.id_User.NumIdent} -- Hora de inicio: {self.hora_inicio} -- Hora de salida: {self.hora_salida}'
        return texto
