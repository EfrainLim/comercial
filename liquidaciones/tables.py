import django_tables2 as tables
from .models import Liquidacion

class LiquidacionTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='liquidaciones/liquidacion_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Liquidacion
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'proveedor__razon_social',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'fecha_creacion'
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        } 