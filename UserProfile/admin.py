from django.contrib import admin
from.models import Nacionalidads, User


from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Administración de Usuarios'
    site_title = 'Panel de Administración'
    index_title = 'Bienvenido al Panel de Administración'

# Register your models here.
admin_site = MyAdminSite(name='myadmin')
# admin.site.register(Nacionalidads)
admin.site.register(User)