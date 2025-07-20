from django import forms
from .models import Ley
from lotes.models import Lote

class LeyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo los lotes que no tienen ley
        if not self.instance.pk:  # Solo para creación nueva
            lote_field = self.fields['lote']
            lote_field.queryset = Lote.objects.filter(ley__isnull=True).select_related('facturador', 'tipo_producto')
            
            # Mejorar las opciones del select para mostrar más información
            lote_field.choices = [('', '---------')] + [
                (lote.id, f"{lote.codigo_lote} - {lote.facturador.razon_social} - {lote.tipo_producto.nombre}")
                for lote in lote_field.queryset
            ]

    class Meta:
        model = Ley
        fields = [
            'lote',
            'porcentaje_h2o',
            'ley_onz_tc',
            'porcentaje_recuperacion',
            'estado'
        ]
        widgets = {
            'lote': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar lote...',
                'style': 'width: 100%;'
            }),
            'porcentaje_h2o': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ejemplo: 4.48'
            }),
            'ley_onz_tc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ejemplo: 0.452'
            }),
            'porcentaje_recuperacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ejemplo: 84.50'
            }),
            'estado': forms.Select(attrs={'class': 'form-control'})
        } 