import django_filters
from django import forms
from .models import Costo

class CostoFilter(django_filters.FilterSet):
    lote__codigo_lote = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Código de Lote'
    )
    lote__facturador__razon_social = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Facturador'
    )
    tipo_analisis = django_filters.ChoiceFilter(
        choices=Costo.TIPOS_ANALISIS,
        label='Tipo de Análisis'
    )
    fecha_creacion = django_filters.DateFromToRangeFilter(
        label='Fecha de Creación',
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Costo
        fields = [
            'lote__codigo_lote',
            'lote__facturador__razon_social',
            'tipo_analisis',
            'estado',
            'fecha_creacion'
        ] 