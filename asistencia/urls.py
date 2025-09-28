from django.urls import path
from .import views

urlpatterns = [
    path('', views.RegisterAsistencia, name='RegisterAsis'),
    path('horario/', views.HorarioCreateView, name='RegisterHorario'),
    path('list/hoy/', views.AsistenciasListView, name='ListAsis'),
    path('list/hoy/pdf/', views.asistencia_list_pdf, name='ListAsisPDF'),
    path('list/hoy/<int:id_user>/<int:id_fecha>', views.Actualizar_Hora_S, name='UpdatetAsis'),
    path('periodo/', views.PeriodoCreateView.as_view(), name='PeriodoForm'),
    path('periodo/delete/<int:id>', views.Eliminar_Periodo, name='PeriodoDelete'),
    path('error/', views.ErrorAdminView.as_view(), name='ErrorAdmin'),
    path('reporte-periodo/', views.reporte_periodo_view, name='reporte_periodo'),
    path('reporte-periodo/pdf/', views.reporte_periodo_view_pdf, name='reporte_periodo_pdf'),
    path('reporte-mensual/', views.reporte_periodo_mes_view, name='reporte_periodo_mes'),
    # path('reporte-semanal/', views.reporte_semanal_view, name='reporte_semanal'),
    path('reporte_mensual/pdf/', views.reporte_periodo_mes_pdf, name='reporte_periodo_mes_pdf'),
]