from django.db import models
from django.utils import timezone
from lotes.models import Lote
from usuarios.models import Usuario
from decimal import Decimal

class Ley(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    ]

    lote = models.OneToOneField(Lote, on_delete=models.CASCADE, verbose_name='Lote')
    tms = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='TMS')
    porcentaje_h2o = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='% H2O')
    ley_onz_tc = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Ley (onz/tc)')
    porcentaje_recuperacion = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='% Recuperación')
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P', verbose_name='Estado')
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='leyes_creadas', verbose_name='Usuario Creador')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Creación')
    usuario_modificador = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name='leyes_modificadas', verbose_name='Usuario Modificador')
    fecha_modificacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Modificación')
    
    class Meta:
        verbose_name = 'Ley'
        verbose_name_plural = 'Leyes'
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"Ley {self.lote.codigo_lote} - {self.get_estado_display()}"
        
    def save(self, *args, **kwargs):
        # Calcular TMS
        tmh = self.lote.tmh
        self.tms = tmh - (tmh * (self.porcentaje_h2o / Decimal('100')))
        
        # Actualizar fecha_ley_agregada en el lote
        self.lote.fecha_ley_agregada = timezone.now()
        self.lote.save()
        
        super().save(*args, **kwargs)
