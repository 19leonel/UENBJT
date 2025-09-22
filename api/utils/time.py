from django.utils import timezone


def fecha_actual():
    fecha = timezone.localtime(timezone.now()).date()
    return fecha


def hora_actual():
    hora_local = timezone.localtime(timezone.now()).strftime('%H:%M:%S')
    return hora_local


def AnoActual():
    anoActual = timezone.localtime(timezone.now()).strftime('%Y')
    fecha_recta = int(anoActual)
    anoAnterior = fecha_recta-1
    formato = f'{anoAnterior}-{anoActual}'
    return formato
