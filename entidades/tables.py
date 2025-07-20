import django_tables2 as tables
from .models import Facturador, Vehiculo, Conductor, ProveedorIngemmet, TipoProducto
from django.utils.safestring import mark_safe

class FacturadorTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='entidades/facturador_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Facturador
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'razon_social',
            'ruc',
            'tipo',
            'direccion',
            'telefono',
            'correo',
            'estado',
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        }

class VehiculoTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='entidades/vehiculo_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Vehiculo
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'placa',
            'tipo',
            'facturador',
            'marca',
            'modelo',
            'estado',
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        }

class ConductorTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='entidades/conductor_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Conductor
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'dni',
            'nombres',
            'licencia_conducir',
            'categoria_licencia',
            'fecha_vencimiento_licencia',
            'empresa',
            'estado',
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        }

class ProveedorIngemmetTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='entidades/proveedor_ingemmet_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = ProveedorIngemmet
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'codigo_ingemmet',
            'procedencia',
            'estado',
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        }

class TipoProductoTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='entidades/tipo_producto_acciones.html',
        verbose_name='Acciones',
        orderable=False
    )
    estado = tables.Column(empty_values=(), orderable=False)
    es_mineral = tables.Column(empty_values=(), orderable=False)
    
    class Meta:
        model = TipoProducto
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nombre', 'descripcion', 'es_mineral', 'estado', 'acciones')
        attrs = {
            'class': 'table table-bordered table-hover',
            'thead': {
                'class': 'table-light',
            },
        }
    
    def render_estado(self, record):
        if record.estado:
            return mark_safe('<span class="badge bg-success">Activo</span>')
        return mark_safe('<span class="badge bg-secondary">Inactivo</span>')
        
    def render_es_mineral(self, record):
        if record.es_mineral:
            return mark_safe('<span class="badge bg-primary">Mineral</span>')
        return mark_safe('<span class="badge bg-secondary">No Mineral</span>') 