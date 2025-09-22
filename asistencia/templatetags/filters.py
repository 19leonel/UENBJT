from django import template
register = template.Library()
import locale


@register.filter
def get_range(value, max_value):
    return range(value, max_value+1)


register = template.Library()

# Diccionarios manuales
DIAS = ['Lunes', 'Martes', 'Miércoles',
        'Jueves', 'Viernes', 'Sábado', 'Domingo']
MESES = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]


@register.filter
def fecha_larga(value):
    """Convierte una fecha tipo 2025-07-02 a 'Miércoles 2 de Julio de 2025'"""
    dias = ['Lunes', 'Martes', 'Miércoles',
            'Jueves', 'Viernes', 'Sábado', 'Domingo']


    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    try:
        dia_semana = dias[value.weekday()]  # weekday: 0=lunes, 6=domingo
        dia = value.day
        mes = meses[value.month - 1]
        anio = value.year
        return f"{dia_semana} {dia} de {mes} de {anio}"
    except Exception:
        return value  # si algo falla, devuelve la fecha normal
