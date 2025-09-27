from collections import defaultdict
from .models import assistance, Periodo, Fecha
from weasyprint import HTML
from django.shortcuts import render, HttpResponse
from .models import assistance
from .utils.time import hora_actual, fecha_actual, AnoActual
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .form import RegisterAssistance, UpdateAssistance, PeriodoForm, FilterAsistencia, HorariosForm
from .models import assistance, Periodo, Fecha, Horarios
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from UserProfile.models import User
import calendar
from datetime import datetime, time, timedelta
# Create your views here.


def formatear_minutos_a_horas_y_minutos(minutos):
    horas = int(minutos // 60)
    mins = int(minutos % 60)
    return f"{horas} horas, {mins} minutos"


def Actualizar_Hora_S(request, id_user, id_fecha):
    dato = assistance.objects.get(id_User=id_user, id_fecha=id_fecha)
    dato.hora_salida = hora_actual()
    dato.save()
    return redirect('ListAsis')


def HorarioCreateView(request):
    # listas = Horarios.objects.all()
    form = HorariosForm()

    if request.method == 'POST':
        id = request.POST['id_user']
        dia = request.POST['Dia']

        # Verificar si ya existe un horario con ese usuario y día
        horario = Horarios.objects.filter(id_user=id, Dia=dia).first()

        listas = Horarios.objects.all()
        user=User.objects.all()
        
        if not horario:
            form = HorariosForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, "asistencia/HorariosForm.html", {
                    'ListHorario': listas,
                    'form': form,
                    'id': id,
                    'usuario':user
                })
        else:
            error = 'El Usuario ya tiene un horario asignado para este día.'
            return render(request, "asistencia/HorariosForm.html", {
                'form': form,
                'error': error,
                'ListHorario': listas,
                'id': id,
                'usuario':user
            })

    return render(request, "asistencia/HorariosForm.html", {
        'form': form,
        'ListHorario': listas,
        'usuario': user
    })
    # def form_invalid(self, form):
    #     print(form.fields)
    #     horario = Horarios.objects.all()
    #     for d in horario:
    #         if form.fields['Dia'] == d.Dia and form.fields['id_user'] == d.id_user:
    #             form.add_error('Usuario y Dia.',
    #                            'Usuario tiene Horario para este Dia.')
    #     return super().form_invalid(form)


class ErrorAdminView(TemplateView):
    template_name = "error/Error.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = 'Error Admin'
        context['message'] = 'No eres Administrador'
        return context


@login_required
def RegisterAsistencia(request):
    if not request.user.is_staff:
        context = {
            'error': 'Error',
            'message': 'No Eres Administrador',
        }
        return render(request, 'error/Error.html', context)
    else:
        fecha = fecha_actual()

        # Obtener o crear la fecha del día
        obj_fecha, _ = Fecha.objects.get_or_create(fecha=fecha)
        form = RegisterAssistance(
            initial={'id_fecha': obj_fecha, 'hora_inicio': hora_actual(), 'id_periodo': Periodo.objects.last()})
        if request.method == 'GET':
            usuario = request.user

            registros_existentes = assistance.objects.filter(
                id_fecha=obj_fecha)
            if not registros_existentes.exists():
                periodo_actual = Periodo.objects.last()
                for user in User.objects.filter(is_active=True):
                    assistance.objects.create(
                        id_User=user,
                        id_fecha=obj_fecha,
                        hora_inicio=None,
                        hora_salida=None,
                        Asis=False,
                        id_periodo=periodo_actual
                    )
            asistencia = assistance.objects.get(
                id_User=usuario, id_fecha=obj_fecha)

            if not asistencia.Asis:
                asistencia.hora_inicio = hora_actual()
                asistencia.Asis = True
                asistencia.save()
            return render(request, "asistencia/RegisterAsis.html", {'form': form})
        else:
            data = request.POST
            id_usuario = data['id_User']
            id_fecha = data['id_fecha']
            hora = data['hora_inicio']
            id_periodo = Periodo.objects.get(id=data['id_periodo'])

            Hora_update = assistance.objects.get(
                id_User=id_usuario, id_fecha=id_fecha)
            if Hora_update.hora_inicio == None and Hora_update.Asis == False:
                Hora_update.hora_inicio = hora
                Hora_update.id_periodo = id_periodo
                Hora_update.Asis = True
                Hora_update.save()
                Exito = 'Hora de Entrada Registrada con Exito'
                return render(request, "asistencia/RegisterAsis.html", {'form': form, 'Exito': Exito})
            elif Hora_update.hora_inicio and Hora_update.Asis == True:
                error = f'El Usuario {Hora_update.id_User.username} tiene Hora de Entrada registrado'
                return render(request, "asistencia/RegisterAsis.html", {'form': form, 'error': error})


def AsistenciasListView(request):
    if request.user.is_staff:
        try:
            idfecha = Fecha.objects.get(fecha=fecha_actual())
        except Fecha.DoesNotExist:
            idfecha = None
        lista = assistance.objects.filter(id_fecha=idfecha)
        if lista.exists():
            for asistencia in lista:
                if asistencia.hora_inicio and asistencia.hora_salida:
                    asistencia.row_class = "table-success"
                elif asistencia.hora_inicio or asistencia.hora_salida:
                    asistencia.row_class = "table-warning"
                else:
                    asistencia.row_class = "table-danger"
            return render(request, 'asistencia/Listasis.html', {'lista': lista, 'asistencia': asistencia})
        else:
            return render(request, 'asistencia/Listasis.html', {'lista': lista,})
    else:
        try:
            idfecha = Fecha.objects.get(fecha=fecha_actual())
        except Fecha.DoesNotExist:
            idfecha= None 
            # return 
        lista = assistance.objects.filter(
            id_fecha=idfecha, id_User=request.user)
        return render(request, 'asistencia/Listasis.html', {'lista': lista})
    

def asistencia_list_pdf(request):
    if request.user.is_staff:
        fecha = Fecha.objects.get(fecha=fecha_actual())
        lista = assistance.objects.filter(id_fecha=fecha)
        for asistencia in lista:
            if asistencia.hora_inicio and asistencia.hora_salida:
                asistencia.row_class = "table-success"
            elif asistencia.hora_inicio or asistencia.hora_salida:
                asistencia.row_class = "table-warning"
            else:
                asistencia.row_class = "table-danger"
        context = {
            'lista': lista,
            'asistencia': asistencia,
            'fecha': fecha,
            }
        html_string=render_to_string('asistencia/ListAsisPDF.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Retornar el PDF como respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="reporte_fecha_{fecha.fecha}.pdf"'
        return response
    else:
        idfecha = Fecha.objects.get(fecha=fecha_actual())
        lista = assistance.objects.filter(
            id_fecha=idfecha, id_User=request.user)
        context = {
            'lista': lista,
            'fecha': fecha,
        }
        html_string = render_to_string('asistencia/ListAsisPDF.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Retornar el PDF como respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="reporte_fecha_{fecha.fecha}.pdf"'
        return response


class PeriodoCreateView(LoginRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = "asistencia/PeriodoCreateView.html"
    success_url = reverse_lazy('PeriodoForm')

    def get_initial(self):
        initial = super().get_initial()
        PeriodoActual = AnoActual()
        initial['periodos'] = PeriodoActual
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ListPeriodo'] = Periodo.objects.all()
        return context

    def form_valid(self, form):
        print(form.as_div())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@login_required
def ReportePorFecha(request, id):
    asistencia = assistance.objects.filter(id_fecha=id)
    if asistencia.exists():
        return render(request, 'asistencia/ReporteFecha.html', {'asistencia': asistencia})
    else:
        error = 'No hay asistencia registrada para esta fecha.'
        return render(request, 'asistencia/ReporteFecha.html', {'error': error})


def formatear_minutos_a_horas_y_minutos(minutos):
    horas = int(minutos // 60)
    min_restantes = int(minutos % 60)
    return f"{horas}h {min_restantes}min"


def reporte_periodo_view(request):
    context = {}

    if request.method == "POST":
        periodo_id = request.POST.get("periodo")

        try:
            periodo = Periodo.objects.get(id=periodo_id)
        except Periodo.DoesNotExist:
            context['error'] = "El período no existe"
            return render(request, 'asistencia/reporte_periodo.html', context)

        registros = assistance.objects.filter(
            id_periodo=periodo
        ).select_related('id_fecha', 'id_User').order_by('id_fecha__fecha')

        # Restricción para usuarios normales (no staff)
        registros_false = assistance.objects.filter(id_periodo=periodo, Asis=False).select_related(
            'id_fecha', 'id_User').count()
        if not request.user.is_staff:
            registros = registros.filter(id_User=request.user)
            registros_false = assistance.objects.filter(
                id_periodo=periodo, Asis=False, id_User=request.user).count()

        asistencias_agrupadas = defaultdict(list)


        for a in registros:
            # try:
            #     dia_semana = a.id_fecha.fecha.strftime('%A').capitalize()
            #     horario = Horarios.objects.get(
            #         id_user=a.id_User, Dia=dia_semana)
            # except Horarios.DoesNotExist:
            #     continue

            

            semana = a.id_fecha.fecha.isocalendar()[1]
            asistencias_agrupadas[semana].append(a)

        resumen = {
            "total": registros.count(),
            "asistencias": registros.filter(Asis=True).count(),
            "inasistencias": registros.filter(Asis=False).count(),
        }

        context.update({
            "asistencias_agrupadas": dict(asistencias_agrupadas),
            "resumen": resumen,
            "periodo_actual": periodo,
        })

    context["Periodos"] = Periodo.objects.all()
    return render(request, 'asistencia/reporte_periodo.html', context)


def reporte_periodo_view_pdf(request):
    context = {}


    periodo_id = request.GET.get("periodo")

    try:
        periodo = Periodo.objects.get(id=periodo_id)
    except Periodo.DoesNotExist:
        context['error'] = "El período no existe"
        return render(request, 'asistencia/reporte_periodo.html', context)

    registros = assistance.objects.filter(
        id_periodo=periodo
    ).select_related('id_fecha', 'id_User').order_by('id_fecha__fecha')

    # Restricción para usuarios normales (no staff)
    registros_false = assistance.objects.filter(id_periodo=periodo, Asis=False).select_related(
        'id_fecha', 'id_User').count()
    if not request.user.is_staff:
        registros = registros.filter(id_User=request.user)
        registros_false = assistance.objects.filter(
            id_periodo=periodo, Asis=False, id_User=request.user).count()

    asistencias_agrupadas = defaultdict(list)

    for a in registros:
        # try:
        #     dia_semana = a.id_fecha.fecha.strftime('%A').capitalize()
        #     horario = Horarios.objects.get(
        #         id_user=a.id_User, Dia=dia_semana)
        # except Horarios.DoesNotExist:
        #     continue

        semana = a.id_fecha.fecha.isocalendar()[1]
        asistencias_agrupadas[semana].append(a)

    resumen = {
        "total": registros.count(),
        "asistencias": registros.filter(Asis=True).count(),
        "inasistencias": registros_false,
    }

    context.update({
        "asistencias_agrupadas": dict(asistencias_agrupadas),
        "resumen": resumen,
        "periodo_actual": periodo,
    })

    html_string = render_to_string(
        'asistencia/reporte_periodo_pdf.html', context)

    # Convertir el HTML a PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Retornar el PDF como respuesta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_periodo_{periodo.periodos}_.pdf"'
    return response

def reporte_periodo_mes_view(request):
    context = {}

    if request.method == "POST":
        periodo_id = request.POST.get("periodo")
        mes = int(request.POST.get("mes"))

        try:
            periodo = Periodo.objects.get(id=periodo_id)
        except Periodo.DoesNotExist:
            context['error'] = "El período no existe"
            return render(request, 'asistencia/reporte_periodo_mes.html', context)

        registros = assistance.objects.filter(
            id_periodo=periodo,
            id_fecha__fecha__month=mes
        ).select_related('id_fecha', 'id_User').order_by('id_fecha__fecha')

        if not request.user.is_staff:
            registros = registros.filter(id_User=request.user)
        # Agrupar por semana
        asistencias_agrupadas = defaultdict(list)
        for a in registros:
            semana = a.id_fecha.fecha.isocalendar()[1]
            asistencias_agrupadas[semana].append(a)

        # Diccionario de días en español
        dias_ingles_a_es = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miercoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }

        # Cálculo de horas culminadas y no culminadas
        total_min_culminadas = 0
        total_min_no_culminadas = 0

        for a in registros:
            if not a.Asis:
                # Si está ausente, mostrar 0 h 0 min
                a.tiempo_culminado = "0 h 0 min"
                a.tiempo_no_culminado = "0 h 0 min"
                continue

            try:
                dia_semana = a.id_fecha.fecha.strftime(
                    '%A').capitalize()  # Ej: "Lunes"
                horario = Horarios.objects.get(
                    id_user=a.id_User, Dia=dia_semana)
            except Horarios.DoesNotExist:
                a.tiempo_culminado = "Horario no asignado"
                a.tiempo_no_culminado = "Horario no asignado"
                continue

            hora_inicio_real = a.hora_inicio
            hora_salida_real = a.hora_salida or time(
                16, 0)  # Si no hay salida, usar 16:00

            entrada_real = datetime.combine(a.id_fecha.fecha, hora_inicio_real)
            salida_real = datetime.combine(a.id_fecha.fecha, hora_salida_real)
            entrada_teorica = datetime.combine(
                a.id_fecha.fecha, horario.Hora_E)
            salida_teorica = datetime.combine(a.id_fecha.fecha, horario.Hora_S)

            tiempo_laborado = salida_real - entrada_real
            tiempo_teorico = salida_teorica - entrada_teorica

            minutos_laborados = max(tiempo_laborado.total_seconds() // 60, 0)
            minutos_teoricos = max(tiempo_teorico.total_seconds() // 60, 0)

            min_culminados = min(minutos_laborados, minutos_teoricos)
            min_no_culminados = max(minutos_teoricos - minutos_laborados, 0)

            total_min_culminadas += min_culminados
            total_min_no_culminadas += min_no_culminados

            # 🔹 Asignar al objeto `a` para que se pueda usar en la plantilla
            a.min_culminados = min_culminados
            a.min_no_culminados = min_no_culminados

            def formatear(minutos):
                horas = int(minutos // 60)
                mins = int(minutos % 60)
                return f"{horas} h {mins} min"

            a.tiempo_culminado = formatear(min_culminados)
            a.tiempo_no_culminado = formatear(min_no_culminados)

        # Preparar resumen
        resumen = {
            "total": registros.count(),
            "asistencias": registros.filter(Asis=True).count(),
            "inasistencias": registros.filter(Asis=False).count(),
            "horas_culminadas": formatear_minutos_a_horas_y_minutos(total_min_culminadas),
            "horas_no_culminadas": formatear_minutos_a_horas_y_minutos(total_min_no_culminadas)
        }

        MESES_ES = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        context.update({
            "asistencias_agrupadas": dict(asistencias_agrupadas),
            "resumen": resumen,
            "periodo_actual": periodo,
            "mes_actual": MESES_ES[mes]
        })

    context["Periodos"] = Periodo.objects.all()
    return render(request, 'asistencia/reporte_periodo_mes.html', context)


@login_required
def reporte_semanal_view(request):
    context = {}

    if request.method == "POST":
        # periodo_id = request.POST.get("periodo")
        periodo_id = 1

        try:
            periodo = Periodo.objects.get(id=1)
        except Periodo.DoesNotExist:
            context['error'] = "El período no existe"
            return render(request, 'asistencia/reporte_semanal.html', context)

        # Filtrar las asistencias del periodo seleccionado
        registros = assistance.objects.filter(id_periodo=periodo).select_related(
            'id_fecha', 'id_User').order_by('id_fecha__fecha')

        # Restricción para usuarios normales (no staff)
        if not request.user.is_staff:
            # Solo mostrar las asistencias del usuario activo
            registros = registros.filter(id_User=request.user)

        asistencias_agrupadas = defaultdict(list)

        total_min_culminadas = 0
        total_min_no_culminadas = 0

        asistencias_agrupadas = defaultdict(list)
        asistencias_contadas = defaultdict(lambda: {
                                           'asistencias': 0, 'inasistencias': 0, 'horas_culminadas': 0, 'horas_no_culminadas': 0})

        for a in registros:
            if not a.Asis:
                continue

            semana = a.id_fecha.fecha.isocalendar()[1]  # Agrupar por semana
            asistencias_agrupadas[semana].append(a)

            if a.Asis:  # Asistencia
                asistencias_contadas[semana]['asistencias'] += 1
            else:  # Inasistencia
                asistencias_contadas[semana]['inasistencias'] += 1

            # Sumar las horas culminadas y no culminadas
            asistencias_contadas[semana]['horas_culminadas'] += a.min_culminados
            asistencias_contadas[semana]['horas_no_culminadas'] += a.min_no_culminados
            # Obtener el día de la semana y el horario teórico
            try:
                dia_semana = a.id_fecha.fecha.strftime('%A').capitalize()
                horario = Horarios.objects.get(
                    id_user=a.id_User, Dia=dia_semana)
            except Horarios.DoesNotExist:
                continue

            entrada_real = datetime.combine(a.id_fecha.fecha, a.hora_inicio)
            salida_real = datetime.combine(
                a.id_fecha.fecha, a.hora_salida or time(16, 0))

            entrada_teorica = datetime.combine(
                a.id_fecha.fecha, horario.Hora_E)
            salida_teorica = datetime.combine(a.id_fecha.fecha, horario.Hora_S)

            # Calcular el tiempo trabajado y el tiempo teórico
            tiempo_laborado = salida_real - entrada_real
            tiempo_teorico = salida_teorica - entrada_teorica

            minutos_laborados = max(tiempo_laborado.total_seconds() // 60, 0)
            minutos_teoricos = max(tiempo_teorico.total_seconds() // 60, 0)

            min_culminados = min(minutos_laborados, minutos_teoricos)
            min_no_culminados = max(minutos_teoricos - minutos_laborados, 0)

            a.min_culminados = min_culminados
            a.min_no_culminados = min_no_culminados
            a.tiempo_culminado = formatear_minutos_a_horas_y_minutos(
                min_culminados)
            a.tiempo_no_culminado = formatear_minutos_a_horas_y_minutos(
                min_no_culminados)

            total_min_culminadas += min_culminados
            total_min_no_culminadas += min_no_culminados

            semana = a.id_fecha.fecha.isocalendar()[1]  # Agrupar por semana
            asistencias_agrupadas[semana].append(a)

        resumen = {
            "total": registros.count(),
            "asistencias": registros.filter(Asis=True).count(),
            "inasistencias": registros.filter(Asis=False).count(),
            "horas_culminadas": formatear_minutos_a_horas_y_minutos(total_min_culminadas),
            "horas_no_culminadas": formatear_minutos_a_horas_y_minutos(total_min_no_culminadas),
        }

        context.update({
            "asistencias_agrupadas": dict(asistencias_agrupadas),
            "resumen": resumen,
            "periodo_actual": periodo,
        })

    context["Periodos"] = Periodo.objects.all()
    return render(request, 'asistencia/reporte_semanal.html', context)

@login_required
def reporte_periodo_mes_pdf(request):
    context = {}

    # if request.method == "POST":
    MESES = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }
    # Obtener los valores de la solicitud GET
    periodo_id = request.GET.get("periodo")
    meses = request.GET.get("mes")
    mes=MESES[meses]

    try:
        # Verificar si el periodo existe
        periodo = Periodo.objects.get(id=periodo_id)
    except Periodo.DoesNotExist:
        # Si no se encuentra el periodo, enviar un error
        context['error'] = "El período no existe"
        return render(request, 'asistencia/reporte_mensual.html', context)

    # Si periodo se encuentra correctamente, continuar con el resto de la lógica
    registros = assistance.objects.filter(
        id_periodo=periodo,
        id_fecha__fecha__month=mes
    ).select_related('id_fecha', 'id_User').order_by('id_fecha__fecha')

    # Agrupar por semana
    asistencias_agrupadas = defaultdict(list)
    for a in registros:
        semana = a.id_fecha.fecha.isocalendar()[1]
        asistencias_agrupadas[semana].append(a)

    # Diccionario de días en español
    dias_ingles_a_es = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miercoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    # Cálculo de horas culminadas y no culminadas
    total_min_culminadas = 0
    total_min_no_culminadas = 0

    for a in registros:
        if not a.Asis:
            # Si está ausente, mostrar 0 h 0 min
            a.tiempo_culminado = "0 h 0 min"
            a.tiempo_no_culminado = "0 h 0 min"
            continue

        try:
            dia_semana = a.id_fecha.fecha.strftime(
                '%A').capitalize()  # Ej: "Lunes"
            horario = Horarios.objects.get(
                id_user=a.id_User, Dia=dia_semana)
        except Horarios.DoesNotExist:
            a.tiempo_culminado = "Horario no asignado"
            a.tiempo_no_culminado = "Horario no asignado"
            continue

        hora_inicio_real = a.hora_inicio
        hora_salida_real = a.hora_salida or time(
            16, 0)  # Si no hay salida, usar 16:00

        entrada_real = datetime.combine(a.id_fecha.fecha, hora_inicio_real)
        salida_real = datetime.combine(a.id_fecha.fecha, hora_salida_real)
        entrada_teorica = datetime.combine(
            a.id_fecha.fecha, horario.Hora_E)
        salida_teorica = datetime.combine(a.id_fecha.fecha, horario.Hora_S)

        tiempo_laborado = salida_real - entrada_real
        tiempo_teorico = salida_teorica - entrada_teorica

        minutos_laborados = max(tiempo_laborado.total_seconds() // 60, 0)
        minutos_teoricos = max(tiempo_teorico.total_seconds() // 60, 0)

        min_culminados = min(minutos_laborados, minutos_teoricos)
        min_no_culminados = max(minutos_teoricos - minutos_laborados, 0)

        total_min_culminadas += min_culminados
        total_min_no_culminadas += min_no_culminados

        # 🔹 Asignar al objeto `a` para que se pueda usar en la plantilla
        a.min_culminados = min_culminados
        a.min_no_culminados = min_no_culminados

        def formatear(minutos):
            horas = int(minutos // 60)
            mins = int(minutos % 60)
            return f"{horas} h {mins} min"

        a.tiempo_culminado = formatear(min_culminados)
        a.tiempo_no_culminado = formatear(min_no_culminados)

    # Preparar resumen
    resumen = {
        "total": registros.count(),
        "asistencias": registros.filter(Asis=True).count(),
        "inasistencias": registros.filter(Asis=False).count(),
        "horas_culminadas": formatear_minutos_a_horas_y_minutos(total_min_culminadas),
        "horas_no_culminadas": formatear_minutos_a_horas_y_minutos(total_min_no_culminadas)
    }

    MESES_ES = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }

    context.update({
        "asistencias_agrupadas": dict(asistencias_agrupadas),
        "resumen": resumen,
        "periodo_actual": periodo,
        "mes_actual": meses,
    })

    # Final del if POST
    # print("Contexto que se pasa a la plantilla:")


    # print(context)
    # Renderizar la plantilla a HTML para PDF
    html_string = render_to_string(
        'asistencia/reporte_mensual.html', context)

    # Convertir el HTML a PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Retornar el PDF como respuesta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_periodo_{periodo.periodos}_{meses}.pdf"'
    return response
