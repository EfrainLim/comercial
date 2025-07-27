import django_tables2 as tables
from .models import Balanza

class BalanzaTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='balanza/balanza_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    
    class Meta:
        model = Balanza
        template_name = "django_tables2/bootstrap5.html"
        fields = [
            'numero_guia_ticket',
            'facturador',
            'vehiculo',
            'conductor',
            'tipo_producto',
            'peso_neto_kg',
            'tipo_empaque',
            'cantidad_sacos',
            'fecha_ingreso',
            'hora_ingreso',
            'fecha_salida',
            'hora_salida',
        ]
        attrs = {
            'class': 'table table-hover',
            'thead': {
                'class': 'table-light',
            },
        } 