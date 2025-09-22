from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .import models


class UserCreationForm2(UserCreationForm):
    """UserCreationForm definition."""
    class Meta:
        model = models.User
        fields = ['username', 'nombre', 'apellido',
                  'email', 'nacionalidad', 'NumIdent', 'NumTel', 'image',]
        widget = {
            'nacionalidad': forms.Select(attrs={'class ': 'select-dark'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})


class ImgUpdateForm(forms.ModelForm):
    """UserCreationForm definition."""

    class Meta:
        model = models.User
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control bg-dark-red form-button', 'onchange': 'previewImage(event)'}),
        }


class loginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={"autofocus": True, 'style': ' background: #000 !important; color: #fff;', 'class': 'form-control'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                   'style': ' background: #000 !important; color: #fff;', 'class': 'form-control'}),
    )
