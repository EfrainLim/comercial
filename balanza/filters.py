import django_filters
from django import forms
from .models import Balanza

class BalanzaFilter(django_filters.FilterSet):
    numero_guia_ticket = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Número de Guía/Ticket',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    facturador = django_filters.CharFilter(
        field_name='facturador__razon_social',
        lookup_expr='icontains',
        label='Facturador',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    vehiculo = django_filters.CharFilter(
        field_name='vehiculo__placa',
        lookup_expr='icontains',
        label='Vehículo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    conductor = django_filters.CharFilter(
        field_name='conductor__nombres',
        lookup_expr='icontains',
        label='Conductor',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    tipo_producto = django_filters.CharFilter(
        field_name='tipo_producto__nombre',
        lookup_expr='icontains',
        label='Tipo de Producto',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_ingreso = django_filters.DateFromToRangeFilter(
        label='Fecha de Ingreso',
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )
    
    class Meta:
        model = Balanza
        fields = [
            'numero_guia_ticket',
            'facturador',
            'vehiculo',
            'conductor',
            'tipo_producto',
            'fecha_ingreso',
        ] 