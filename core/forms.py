from django import forms
from .models import Cotizacion
from servicios.models import Servicio


class CotizacionForm(forms.ModelForm):
    # Honeypot: campo invisible para humanos. Si viene lleno, es un bot.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Cotizacion
        fields = ['nombre', 'telefono', 'email', 'comuna', 'servicio', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Tu nombre'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+56 9 1234 5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.cl (opcional)'
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: Maipú'
            }),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Contanos qué necesitás: tipo de vehículo, m² aproximados, etc.'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(
            activo=True
        ).select_related('categoria')
        self.fields['servicio'].empty_label = 'No estoy seguro / Otro'
        self.fields['servicio'].required = False

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        solo_digitos = ''.join(c for c in telefono if c.isdigit())
        if len(solo_digitos) < 8:
            raise forms.ValidationError('Ingresá un teléfono válido con al menos 8 dígitos.')
        return telefono

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Error de validación.')
        return ''