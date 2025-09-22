from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Nacionalidads(models.Model):
    Nacionalidad=models.CharField(max_length=500, null=False, blank=False)
    def __str__(self):
        return self.Nacionalidad

class User(AbstractUser):
    nombre=models.CharField(max_length=150, null=True, blank=True, verbose_name="Nombres")
    apellido=models.CharField(max_length=150, null=True, blank=True, verbose_name="Apellidos")
    email_verify = models.BooleanField('Correo Verificado',default=False)
    nacionalidad=models.ForeignKey(Nacionalidads, on_delete=models.CASCADE, verbose_name="Pais", null=True, blank=True)
    NumIdent=models.CharField(max_length=35, null=True, blank=True, verbose_name="Numero de Identidad")
    NumTel= models.CharField(max_length=50, null=True, blank=True, verbose_name="Teléfono")
    NumTel_verify = models.BooleanField('Numero de Telefono Verificado',default=False)
    image = models.ImageField("Imagen de Perfil", upload_to='perfil/%Y-%m-%D %H-%M-%S', default='Usuario.jpg', blank=True, null=True)
    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

    def __str__(self):
        if self.NumIdent == None:
            texto = f'Nombre y Apellido: {self.nombre}. { self.apellido }.  -- Cedula: No tiene registrado'
            return texto
        else:
            texto = f'Nombre y Apellido: {self.nombre}. { self.apellido }.  -- Cedula: {self.NumIdent}'
            return texto
    # def __iter__(self):
    #     return iter([self.username, self.email, self.password])
