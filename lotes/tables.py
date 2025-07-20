import django_tables2 as tables
from .models import Lote, Campana

class LoteTable(tables.Table):
    codigo_lote = tables.Column(verbose_name='Código Lote')
    fecha_ingreso = tables.DateColumn(format='d/m/Y', verbose_name='Fecha Ingreso')
    facturador = tables.Column(verbose_name='Facturador')
    tipo_producto = tables.Column(verbose_name='Tipo Producto')
    tmh = tables.Column(verbose_name='TMH')
    nro_sacos = tables.Column(verbose_name='Nro. Sacos')
    estado = tables.Column(verbose_name='Estado')
    acciones = tables.TemplateColumn(
        template_name='lotes/lote_acciones.html',
        verbose_name='Acciones',
        orderable=False
    )

    class Meta:
        model = Lote
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'codigo_lote',
            'fecha_ingreso',
            'facturador',
            'tipo_producto',
            'tmh',
            'nro_sacos',
            'estado',
            'acciones'
        )
        attrs = {
            'class': 'table table-striped table-bordered',
            'thead': {
                'class': 'thead-dark'
            }
        }
        row_attrs = {
            'class': lambda record: 'table-success' if record.estado == 'activo' else 'table-secondary'
        }

class CampanaTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='lotes/campana_acciones.html',
        verbose_name='Acciones',
        orderable=False
    )

    class Meta:
        model = Campana
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            'nombre',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'acciones',
        )
        attrs = {
            'class': 'table table-bordered table-hover table-striped',
            'thead': {'class': 'table-light'},
        } 