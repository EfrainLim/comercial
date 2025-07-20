from django import forms
from django.utils import timezone
from .models import Liquidacion, LiquidacionDetalle
from lotes.models import Lote
from entidades.models import Facturador
from django.contrib import messages

class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = [
            'proveedor',
            'fecha_inicio',
            'fecha_fin',
            'estado'
        ]
        widgets = {
            'proveedor': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar proveedor...',
                'style': 'width: 100%;'
            }),
            'fecha_inicio': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'fecha_fin': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mejorar las opciones del campo proveedor
        proveedor_field = self.fields['proveedor']
        proveedor_field.queryset = Facturador.objects.all().order_by('razon_social')
        
        # Mejorar las opciones del select para mostrar razón social y RUC
        proveedor_field.choices = [('', '---------')] + [
            (facturador.id, f"{facturador.razon_social} - {facturador.ruc}")
            for facturador in proveedor_field.queryset
        ]
        
        # Asegurar que las fechas se muestren en el formato correcto
        if self.instance.pk:
            if self.instance.fecha_inicio:
                self.initial['fecha_inicio'] = self.instance.fecha_inicio.strftime('%Y-%m-%d')
            if self.instance.fecha_fin:
                self.initial['fecha_fin'] = self.instance.fecha_fin.strftime('%Y-%m-%d')

    def save(self, commit=True, user=None, request=None):
        liquidacion = super().save(commit=False)
        
        if user:
            if not liquidacion.pk:  # Nueva liquidación
                liquidacion.usuario_creador = user
            else:
                liquidacion.usuario_modificador = user
        
        if commit:
            liquidacion.save()
        
        return liquidacion

class LiquidacionDetalleForm(forms.ModelForm):
    class Meta:
        model = LiquidacionDetalle
        fields = [
            'lote',
            'monto_pagado'
        ]
        widgets = {
            'lote': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar lote...',
                'style': 'width: 100%;'
            }),
            'monto_pagado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mejorar las opciones del campo lote
        lote_field = self.fields['lote']
        lote_field.queryset = Lote.objects.filter(
            valorizacion__isnull=False,
            liquidacion__isnull=True
        ).select_related('facturador', 'tipo_producto').order_by('codigo_lote')
        
        # Mejorar las opciones del select para mostrar más información
        lote_field.choices = [('', '---------')] + [
            (lote.id, f"{lote.codigo_lote} - {lote.facturador.razon_social} - {lote.tipo_producto.nombre}")
            for lote in lote_field.queryset
        ] 