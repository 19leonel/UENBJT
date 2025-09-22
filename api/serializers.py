from rest_framework import serializers
from UserProfile.models import User
from asistencia.models import assistance, Fecha, Periodo


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'image',
                  'nombre', 'apellido', 'is_staff']


class FechaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Fecha
        fields = ['id', 'fecha']


class PeriodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'periodos']


class assistanceSerializers(serializers.ModelSerializer):
    id_User = UserSerializers(read_only=True)
    id_fecha = FechaSerializers(read_only=True)
    id_periodo = PeriodoSerializers(read_only=True)

    class Meta:
        model = assistance
        fields = ['id_User', 'id_fecha', 'id_periodo', 'hora_inicio', 'hora_salida', 'Asis',]
