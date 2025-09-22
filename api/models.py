from django.db import models
from UserProfile.models import User

# Create your models here.

class Theme(models.Model):
    """Model definition for Theme."""

    # TODO: Define fields here
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField('Theme', max_length=50, default='light')

    class Meta:
        """Meta definition for Theme."""

        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'

    def __str__(self):
        """Unicode representation of Theme."""
        pass
