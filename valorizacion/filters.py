import django_filters
from django import forms
from .models import Valorizacion
from datetime import datetime, time

class ValorizacionFilter(django_filters.FilterSet):
    lote = django_filters.CharFilter(
        field_name='lote__codigo_lote',
        lookup_expr='icontains',
        label='Código de Lote',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    condicion = django_filters.CharFilter(
        field_name='lote__facturador__razon_social',
        lookup_expr='icontains',
        label='Razón Social',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_desde = django_filters.DateFilter(
        field_name='fecha_creacion',
        lookup_expr='gte',
        label='Fecha Desde',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        method='filter_fecha_desde'
    )
    fecha_hasta = django_filters.DateFilter(
        field_name='fecha_creacion',
        lookup_expr='lte',
        label='Fecha Hasta',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        method='filter_fecha_hasta'
    )
    
    def filter_fecha_desde(self, queryset, name, value):
        if value:
            # Convertir la fecha a datetime con hora 00:00:00
            fecha_desde = datetime.combine(value, time.min)
            return queryset.filter(fecha_creacion__gte=fecha_desde)
        return queryset

    def filter_fecha_hasta(self, queryset, name, value):
        if value:
            # Convertir la fecha a datetime con hora 23:59:59
            fecha_hasta = datetime.combine(value, time.max)
            return queryset.filter(fecha_creacion__lte=fecha_hasta)
        return queryset
    
    class Meta:
        model = Valorizacion
        fields = [
            'lote',
            'condicion',
            'fecha_desde',
            'fecha_hasta'
        ] 