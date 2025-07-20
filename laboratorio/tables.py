import django_tables2 as tables
from .models import Ley

class LeyTable(tables.Table):
    acciones = tables.TemplateColumn(
        template_name='laboratorio/ley_acciones.html',
        orderable=False,
        verbose_name='Acciones'
    )
    lote = tables.Column(
        accessor='lote.codigo_lote',
        verbose_name='Lote'
    )
    tms = tables.Column(
        verbose_name='TMS'
    )
    porcentaje_h2o = tables.Column(
        verbose_name='% H2O'
    )
    ley_onz_tc = tables.Column(
        verbose_name='Ley (onz/tc)'
    )
    porcentaje_recuperacion = tables.Column(
        verbose_name='% Recuperación'
    )
    estado = tables.Column(
        verbose_name='Estado'
    )
    fecha_creacion = tables.DateTimeColumn(
        format='d/m/Y H:i',
        verbose_name='Fecha Registro'
    )

    class Meta:
        model = Ley
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'lote',
            'tms',
            'porcentaje_h2o',
            'ley_onz_tc',
            'porcentaje_recuperacion',
            'estado',
            'fecha_creacion',
            'acciones'
        )
        attrs = {
            'class': 'table table-bordered table-striped table-hover',
            'thead': {
                'class': 'thead-dark'
            }
        }
        row_attrs = {
            'class': lambda record: 'table-success' if record.estado == 'A' else 'table-warning' if record.estado == 'P' else 'table-danger'
        } 