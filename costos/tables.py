import django_tables2 as tables
from .models import Costo

class CostoTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='costos/costo_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Costo
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'lote__codigo_lote',
            'lote__facturador__razon_social',
            'pio_us_onza',
            'rc',
            'maquila',
            'consumo_adicional',
            'analisis_newmonth',
            'tipo_analisis',
            'analisis_usd',
            'precio_usd_tms',
            'humedad_lab',
            'tms_real',
            'ley_lab',
            'estado',
            'fecha_creacion'
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        } 