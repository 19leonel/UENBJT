
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .serializers import UserSerializers, User, Fecha, FechaSerializers, assistance, assistanceSerializers, Periodo, PeriodoSerializers
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from django.http import Http404
from .utils.time import AnoActual, fecha_actual, hora_actual
from asistencia.views import formatear_minutos_a_horas_y_minutos
from collections import defaultdict
from datetime import date

# Create your views here.


@api_view(['POST'])
def login(request):
    if request.data:
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"error": "Credenciales Inválido"}, status=HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializers(instance=user)

        return Response({"token": token.key, "user": serializer.data, "Session": True}, status=HTTP_200_OK)
    else:
        return Response({})


@api_view(['POST'])
def AsistenciaApiList(request):
    if request.data:
        try:
            fecha = get_object_or_404(Fecha, fecha=fecha_actual())
            fecha_serializado = FechaSerializers(fecha)
            lista = assistance.objects.filter(
                id_fecha=fecha, id_User=request.data['id'])
            serializer = assistanceSerializers(lista, many=True,)
            return Response(serializer.data, status=HTTP_200_OK)
        except Http404:
            raise Http404('No hay registro para esta Fecha')
    else:
        return Response({})


@api_view(['POST'])
def AsistenciaSemanalApiList(request):
    user = request.data['id']
    asistencias = assistance.objects.filter(
        id_User=user).order_by('id_fecha__fecha')
    semanas = defaultdict(list)
    for a in asistencias:
        semana = a.id_fecha.fecha.isocalendar()[1]
        ano = a.id_fecha.fecha.isocalendar()[0]
        semanas[(ano, semana)].append(a)

        resultado = []
        for (ano, semana), registros in semanas.items():
            serializer = assistanceSerializers(registros, many=True)
            resultado.append({
                "ano": ano,
                "semana": semana,
                "total_asistencias": len(serializer.data),
                'registros': serializer.data
            })
            return Response(resultado, status=HTTP_200_OK)


@api_view(['GET'])
def AsistenciaMesApiList(request):
    context = {}
    if request.data:
        id_periodo = request.data['id_periodo']
        mes = request.data['mes']
        id_user = request.data['id_user']
        print(id_periodo)
        print(mes)
        print(id_user)
        try:
            periodo = Periodo.objects.get(id=id_periodo)
        except Periodo.DoesNotExist:
            return Response({"detail": "El periodo no existe"}, status=HTTP_404_NOT_FOUND)

        registros = assistance.objects.filter(id_periodo=id_periodo, id_fecha__fecha__month=mes, id_User=id_user).select_related(
            'id_fecha', 'id_User').order_by('id_fecha__fecha')
        
        asistencias_agrupadas = defaultdict(list)
        for a in registros:
            semana = a.id_fecha.fecha.isocalendar()[1]
            asistencias_agrupadas[semana].append(a)

        resumen = {
            'total': registros.count(),
            'asistencias': registros.filter(Asis=True).count(),
            'inasistencias': registros.filter(Asis=False).count(),
        }

        MESES_ES = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        p = PeriodoSerializers(periodo)

        asistencias_agrupadas_serializada = {}
        for semana, asistencias in asistencias_agrupadas.items():
            serializer = assistanceSerializers(asistencias, many=True)
            asistencias_agrupadas_serializada[semana] = serializer.data

        context.update(
            {
                "asistencias_agrupadas": asistencias_agrupadas_serializada,
                "resumen": resumen,
                "periodo_actual": p.data,
                "mes_actual": MESES_ES[mes]
            }
        )
        return Response(context, status=HTTP_200_OK)
    else:
        periodos = Periodo.objects.all()
        p = PeriodoSerializers(periodos, many=True)

        return Response(p.data, status=HTTP_200_OK)


@api_view(['GET'])
def AsistenciaPeriodoApiList(request):
    context = {}

    if request.data:
        id_periodo = request.data["id_periodo"]
        id_user = request.data["id_user"]
        try:
            periodo = Periodo.objects.get(id=id_periodo)
        except Periodo.DoesNotExist:
            return Response({'detail': "El período no existe"}, status=HTTP_404_NOT_FOUND)

        registros = assistance.objects.filter(id_periodo=periodo, id_User=id_user).select_related(
            'id_fecha', 'id_User').order_by('id_fecha__fecha')
        registros_false = assistance.objects.filter(
            id_periodo=periodo, id_User=id_user, Asis=False).count()

        asistencias_agrupadas = {}
        for a in registros:
            mes = a.id_fecha.fecha.month
            semana = a.id_fecha.fecha.isocalendar()[1]
            if mes not in asistencias_agrupadas:
                asistencias_agrupadas[mes] = {}
            if semana not in asistencias_agrupadas[mes]:
                asistencias_agrupadas[mes][semana] = []
            asistencias_agrupadas[mes][semana].append({
                'id_User': {
                    'id': a.id_User.pk,
                    'nombre': a.id_User.nombre,
                    'apellido': a.id_User.apellido,
                    },
                'id_fecha': {
                    'id':a.id_fecha.pk,
                    'fecha':a.id_fecha.fecha
                    },
                'hora_inicio': a.hora_inicio,
                'hora_salida': a.hora_salida,
                'Asis': a.Asis,
            })

        asistencias_agrupadas_serializada = {}
        for mes, semanas in asistencias_agrupadas.items():
            asistencias_agrupadas_serializada[str(mes)] ={}
            for semana, asistencias in semanas.items():
                asistencias_agrupadas_serializada[str(mes)][str(semana)]=asistencias

        resumen = {
            "total": registros.count(),
            "asistencias": registros.filter(Asis=True).count(),
            "inasistencias": registros_false,
        }
        periodo_serializado = PeriodoSerializers(periodo).data

        context.update({
            "asistencias_agrupadas": asistencias_agrupadas_serializada,
            "resumen": resumen,
            "periodo_actual": periodo_serializado,
        })
        return Response(context, status=HTTP_200_OK)
    else:
        periodo = Periodo.objects.all()
        periodo_serializado = PeriodoSerializers(periodo, many=True).data
        return Response(periodo_serializado, status=HTTP_200_OK)
