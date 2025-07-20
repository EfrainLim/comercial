from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('balanza', 'Reporte de Balanza'),
        ('campanas', 'Reporte de Campañas'),
        ('lotes', 'Reporte de Lotes'),
        ('leyes', 'Reporte de Leyes'),
        ('costos', 'Reporte de Costos'),
        ('valorizaciones', 'Reporte de Valorizaciones'),
        ('liquidaciones', 'Reporte de Liquidaciones'),
    ]

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_REPORTE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    filtros = models.JSONField(default=dict, blank=True)
    archivo = models.FileField(upload_to='reportes/', null=True, blank=True)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"
