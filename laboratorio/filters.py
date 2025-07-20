import django_filters
from django import forms
from .models import Ley

class LeyFilter(django_filters.FilterSet):
    lote = django_filters.CharFilter(
        field_name='lote__codigo_lote',
        lookup_expr='icontains',
        label='Lote'
    )
    fecha_registro_desde = django_filters.DateFilter(
        field_name='fecha_creacion',
        lookup_expr='date__gte',
        label='Fecha Registro Desde',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_registro_hasta = django_filters.DateFilter(
        field_name='fecha_creacion',
        lookup_expr='date__lte',
        label='Fecha Registro Hasta',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    estado = django_filters.ChoiceFilter(
        choices=Ley.ESTADO_CHOICES,
        label='Estado'
    )
    
    class Meta:
        model = Ley
        fields = [
            'lote',
            'fecha_registro_desde',
            'fecha_registro_hasta',
            'estado'
        ] 