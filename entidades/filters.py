import django_filters
from .models import Facturador, Vehiculo, Conductor, ProveedorIngemmet

class FacturadorFilter(django_filters.FilterSet):
    razon_social = django_filters.CharFilter(
        field_name='razon_social',
        lookup_expr='icontains',
        label='Razón Social'
    )
    ruc = django_filters.CharFilter(
        field_name='ruc',
        lookup_expr='icontains',
        label='RUC'
    )
    tipo = django_filters.CharFilter(
        field_name='tipo',
        lookup_expr='icontains',
        label='Tipo'
    )
    direccion = django_filters.CharFilter(
        field_name='direccion',
        lookup_expr='icontains',
        label='Dirección'
    )
    telefono = django_filters.CharFilter(
        field_name='telefono',
        lookup_expr='icontains',
        label='Teléfono'
    )
    correo = django_filters.CharFilter(
        field_name='correo',
        lookup_expr='icontains',
        label='Correo'
    )
    
    class Meta:
        model = Facturador
        fields = [
            'razon_social',
            'ruc',
            'tipo',
            'direccion',
            'telefono',
            'correo',
        ]

class VehiculoFilter(django_filters.FilterSet):
    placa = django_filters.CharFilter(
        field_name='placa',
        lookup_expr='icontains',
        label='Placa'
    )
    tipo = django_filters.CharFilter(
        field_name='tipo',
        lookup_expr='icontains',
        label='Tipo'
    )
    facturador = django_filters.ModelChoiceFilter(
        queryset=Facturador.objects.all(),
        label='Facturador'
    )
    marca = django_filters.CharFilter(
        field_name='marca',
        lookup_expr='icontains',
        label='Marca'
    )
    modelo = django_filters.CharFilter(
        field_name='modelo',
        lookup_expr='icontains',
        label='Modelo'
    )
    estado = django_filters.ChoiceFilter(
        field_name='estado',
        choices=[(True, 'Activo'), (False, 'Inactivo')],
        label='Estado'
    )
    
    class Meta:
        model = Vehiculo
        fields = [
            'placa',
            'tipo',
            'facturador',
            'marca',
            'modelo',
            'estado',
        ]

class ConductorFilter(django_filters.FilterSet):
    dni = django_filters.CharFilter(
        field_name='dni',
        lookup_expr='icontains',
        label='DNI'
    )
    nombres = django_filters.CharFilter(
        field_name='nombres',
        lookup_expr='icontains',
        label='Nombres'
    )
    categoria_licencia = django_filters.CharFilter(
        field_name='categoria_licencia',
        lookup_expr='icontains',
        label='Categoría de Licencia'
    )
    
    class Meta:
        model = Conductor
        fields = ['dni', 'nombres', 'categoria_licencia']

class ProveedorIngemmetFilter(django_filters.FilterSet):
    codigo_ingemmet = django_filters.CharFilter(
        field_name='codigo_ingemmet',
        lookup_expr='icontains',
        label='Código INGEMMET'
    )
    procedencia = django_filters.CharFilter(
        field_name='procedencia',
        lookup_expr='icontains',
        label='Procedencia'
    )
    estado = django_filters.ChoiceFilter(
        field_name='estado',
        choices=[(True, 'Activo'), (False, 'Inactivo')],
        label='Estado'
    )
    
    class Meta:
        model = ProveedorIngemmet
        fields = [
            'codigo_ingemmet',
            'procedencia',
            'estado',
        ] 