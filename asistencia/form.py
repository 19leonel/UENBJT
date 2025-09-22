from django import forms
from .models import assistance, Periodo, Horarios
from datetime import date, datetime


class RegisterAssistance(forms.ModelForm):
    """UserCreationForm definition."""
    class Meta:
        model = assistance
        fields = ['id_User', 'id_fecha', 'hora_inicio', 'id_periodo']
        widgets = {
            'id_fecha': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time' , 'readonly': 'readonly'}),
            'id_periodo': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('hora_inicio')
        salida = cleaned_data.get('hora_salida')

        if entrada and salida and salida <= entrada:
            raise forms.ValidationError(
                "La hora de salida debe ser posterior a la hora de entrada.")

class UpdateAssistance(forms.ModelForm):
    class Meta:
        model = assistance
        fields = ['id_User', 'id_fecha', 'hora_inicio', 'hora_salida']
        widgets = {
            'id_User': forms.TextInput(attrs={'class': 'form-control'}),
            'id_fecha': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'hora_inicio': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'hora_salida': forms.TextInput(attrs={'class': 'form-control', 'type': 'time', 'readonly': 'readonly'}),

        }


class PeriodoForm(forms.ModelForm):
    """Form definition for Periodo."""

    class Meta:
        """Meta definition for Periodoform."""

        model = Periodo
        fields = ('periodos',)
        widgets = {
            'periodos': forms.TextInput(attrs={'class': 'form-control bg-dark-red form-button'})
        }


class FilterAsistencia(forms.Form):
    """FilterAsistencia definition."""

    # TODO: Define form fields here
    periodo = forms.ModelChoiceField(queryset=Periodo.objects.all().distinct(
    ), widget=forms.Select(attrs={'style': ' background: #000 !important; color: #fff;', 'class': 'form-control'}))
    mes = forms.ChoiceField(choices=[(i, i) for i in range(0, 13)], widget=forms.Select(
        attrs={'style': ' background: #000 !important; color: #fff;', 'class': 'form-control'}))


class HorariosForm(forms.ModelForm):
    """Form definition for Horarios."""

    class Meta:
        """Meta definition for Horariosform."""

        model = Horarios
        fields = '__all__'
        widgets = {
            'id_user': forms.Select(attrs={'class': 'form-control'}),
            'Dia': forms.Select(attrs={'class': 'form-control'}),
            'Hora_E': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'Hora_S': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def Dia_id(self, id):
        dias_disponible = Horarios.get_dias_disponible(id)
        self.fields['Dia'].choices = [
            (dia, dia.capitalize()) for dia in dias_disponible]
