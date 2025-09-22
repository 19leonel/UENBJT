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
from django.urls import path, include
from.import views
from django.conf import settings
from django.contrib.auth.views import LoginView

urlpatterns = [
    
    # INICIO
    path('', views.index, name=""),
    path('profile/', views.perfil, name="index"),
    path('Task/', views.taskView, name="task"),
    path('user/', views.UserViews.as_view(), name="UserList"),
    
    # LOGUEO ,REGISTRO Y lOGOUT DE USUARIO,
    path('login/', LoginView.as_view(), name="login"),
    path('SignUp/', views.UserCreateView.as_view(), name='register'),
    path('logout', views.SigNout, name='logout'),
    
    # OPCION DE PERFIL
    path('profile/cambiar_img/<int:pk>', views.UserUpdateView.as_view(), name='cambiar_img'),
    #path('profile/cambiar_img/<int:id>', views.Cambiar_Img, name='cambiar_img'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )