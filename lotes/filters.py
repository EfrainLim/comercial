import django_filters
from django import forms
from .models import Lote, Campana

class LoteFilter(django_filters.FilterSet):
    codigo = django_filters.CharFilter(
        field_name='codigo_lote',
        lookup_expr='icontains',
        label='Código'
    )
    proveedor = django_filters.CharFilter(
        field_name='facturador__razon_social',
        lookup_expr='icontains',
        label='Proveedor'
    )
    fecha_desde = django_filters.DateFilter(
        field_name='fecha_ingreso',
        lookup_expr='gte',
        label='Desde',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_hasta = django_filters.DateFilter(
        field_name='fecha_ingreso',
        lookup_expr='lte',
        label='Hasta',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Lote
        fields = [
            'codigo',
            'proveedor',
            'fecha_desde',
            'fecha_hasta',
        ]

class CampanaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(
        field_name='nombre',
        lookup_expr='icontains',
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    estado = django_filters.ChoiceFilter(
        choices=Campana.ESTADOS,
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = django_filters.DateFilter(
        field_name='fecha_inicio',
        lookup_expr='gte',
        label='Fecha Inicio Desde',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin = django_filters.DateFilter(
        field_name='fecha_fin',
        lookup_expr='lte',
        label='Fecha Fin Hasta',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Campana
        fields = ['nombre', 'estado', 'fecha_inicio', 'fecha_fin'] 