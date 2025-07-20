import django_tables2 as tables
from .models import Valorizacion

class ValorizacionTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='valorizacion/valorizacion_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Valorizacion
        template_name = "django_tables2/bootstrap4.html"
        fields = [
            'lote__codigo_lote',
            'lote__facturador__razon_social',
            'condicion',
            'comprobante',
            'factura_nro',
            'monto_pagar',
            'fecha_creacion'
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        } 