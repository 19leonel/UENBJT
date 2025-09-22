"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .import settings
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('UserProfile.urls')),
    path('asistencia/', include('asistencia.urls')),
    path('error/', include('asistencia.Error')),
    
    # Rest-Api
    
    re_path('api/login', views.login),
    re_path('api/asistencia/hoy', views.AsistenciaApiList),
    re_path('api/asistencia/semana', views.AsistenciaSemanalApiList),
    re_path('api/asistencia/mes', views.AsistenciaMesApiList),
    re_path('api/asistencia/periodo', views.AsistenciaPeriodoApiList),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
