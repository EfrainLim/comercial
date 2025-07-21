from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['tipo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el tipo de reporte'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'placeholder': 'Fecha de inicio'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'placeholder': 'Fecha de fin'
            }),
        }
        labels = {
            'tipo': 'Tipo de Reporte',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
        }
        help_texts = {
            'tipo': 'Selecciona el tipo de reporte que deseas generar',
            'fecha_inicio': 'Fecha desde la cual incluir datos',
            'fecha_fin': 'Fecha hasta la cual incluir datos',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        
        return cleaned_data

    def save(self, commit=True):
        reporte = super().save(commit=False)
        # Generar título automáticamente
        tipo_display = dict(Reporte.TIPOS_REPORTE)[reporte.tipo]
        reporte.titulo = f"{tipo_display} - {reporte.fecha_inicio} a {reporte.fecha_fin}"
        if commit:
            reporte.save()
        return reporte 