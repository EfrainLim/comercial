from django import forms
from .models import Costo
from lotes.models import Lote
from laboratorio.models import Ley

class CostoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es una edición, mostrar el lote actual
        if self.instance.pk:
            lote_field = self.fields['lote']
            lote_field.queryset = Lote.objects.filter(pk=self.instance.lote.pk).select_related('facturador', 'tipo_producto')
            
            # Mejorar las opciones del select para mostrar más información
            lote_field.choices = [('', '---------')] + [
                (lote.id, f"{lote.codigo_lote} - {lote.facturador.razon_social} - {lote.tipo_producto.nombre}")
                for lote in lote_field.queryset
            ]
        else:
            # Si es un nuevo costo, filtrar lotes disponibles
            lote_field = self.fields['lote']
            lote_field.queryset = Lote.objects.filter(
                ley__isnull=False
            ).exclude(
                costo__isnull=False
            ).select_related('facturador', 'tipo_producto')
            
            # Mejorar las opciones del select para mostrar más información
            lote_field.choices = [('', '---------')] + [
                (lote.id, f"{lote.codigo_lote} - {lote.facturador.razon_social} - {lote.tipo_producto.nombre}")
                for lote in lote_field.queryset
            ]
        
        # Agregar el evento onchange al campo tipo_analisis
        self.fields['tipo_analisis'].widget.attrs.update({
            'onchange': 'actualizarAnalisisUSD(this.value)',
            'class': 'form-control'
        })

    def clean_lote(self):
        lote = self.cleaned_data.get('lote')
        if lote:
            # Si es un nuevo costo, verificar que el lote no tenga costo
            if not self.instance.pk and Costo.objects.filter(lote=lote).exists():
                raise forms.ValidationError('Este lote ya tiene un costo asociado.')
            
            # Verificar si el lote tiene una ley
            if not Ley.objects.filter(lote=lote).exists():
                raise forms.ValidationError('Este lote no tiene una ley asociada. Debe agregar una ley antes de crear el costo.')
        
        return lote

    class Meta:
        model = Costo
        fields = [
            'lote',
            'pio_us_onza',
            'rc',
            'maquila',
            'consumo_adicional',
            'analisis_newmonth',
            'tipo_analisis',
            'analisis_usd',
            'estado'
        ]
        widgets = {
            'lote': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar lote...',
                'style': 'width: 100%;'
            }),
            'pio_us_onza': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 3277.30'}),
            'rc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 200'}),
            'maquila': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 110'}),
            'consumo_adicional': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 25'}),
            'analisis_newmonth': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 25'}),
            'analisis_usd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 25'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        } 