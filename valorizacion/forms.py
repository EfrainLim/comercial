from django import forms
from .models import Valorizacion
from lotes.models import Lote

class ValorizacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es una edición (instance tiene pk), mostrar el lote actual
        if self.instance.pk:
            lote_field = self.fields['lote']
            lote_field.queryset = Lote.objects.filter(pk=self.instance.lote.pk).select_related('facturador', 'tipo_producto')
            
            # Mejorar las opciones del select para mostrar más información
            lote_field.choices = [('', '---------')] + [
                (lote.id, f"{lote.codigo_lote} - {lote.facturador.razon_social} - {lote.tipo_producto.nombre}")
                for lote in lote_field.queryset
            ]
        else:
            # Si es una creación, mostrar solo lotes sin valorización que tengan ley y costo
            lote_field = self.fields['lote']
            lote_field.queryset = Lote.objects.filter(
                valorizacion__isnull=True,
                ley__isnull=False,
                costo__isnull=False
            ).select_related('facturador', 'tipo_producto')
            
            # Mejorar las opciones del select para mostrar más información
            lote_field.choices = [('', '---------')] + [
                (lote.id, f"{lote.codigo_lote} - {lote.facturador.razon_social} - {lote.tipo_producto.nombre}")
                for lote in lote_field.queryset
            ]
            
            # Valores por defecto
            self.fields['condicion'].initial = 'F'
            self.fields['comprobante'].initial = 'FACT'

    class Meta:
        model = Valorizacion
        fields = [
            'lote',
            'condicion',
            'comprobante',
            'factura_nro',
            'pu_tmh_flete',
            'reintegro',
            'anticipo',
            'banco',
            'cuenta',
            'estado'
        ]
        widgets = {
            'lote': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar lote...',
                'style': 'width: 100%;'
            }),
            'condicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: F'}),
            'comprobante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: FACT'}),
            'factura_nro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: E001-85 o BLANCO'}),
            'pu_tmh_flete': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 10 o 0'}),
            'reintegro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 424.4 o BLANCO'}),
            'anticipo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ejemplo: 1770 o BLANCO'}),
            'banco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: BCP'}),
            'cuenta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 44003443493490949 o CCI'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        } 