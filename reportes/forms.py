from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'filtros']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'filtros': forms.HiddenInput(),
        } 