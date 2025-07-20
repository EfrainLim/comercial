from django.db import models
from django.utils import timezone
from entidades.models import Facturador
from lotes.models import Lote
from usuarios.models import Usuario

class Liquidacion(models.Model):
    ESTADOS = (
        ('borrador', 'Borrador'),
        ('finalizada', 'Finalizada'),
        ('anulada', 'Anulada'),
    )
    
    proveedor = models.ForeignKey(Facturador, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='liquidaciones_creadas')
    usuario_modificador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='liquidaciones_modificadas', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Liquidación'
        verbose_name_plural = 'Liquidaciones'
        
    def __str__(self):
        return f"Liquidación {self.id} - {self.proveedor.razon_social}"
    
    def finalizar(self):
        if self.estado == 'borrador':
            self.estado = 'finalizada'
            self.save()
            
            # Marcar lotes como liquidados
            for detalle in self.detalles.all():
                lote = detalle.lote
                lote.fecha_liquidacion_agregada = timezone.now()
                lote.save()

class LiquidacionDetalle(models.Model):
    liquidacion = models.ForeignKey(Liquidacion, on_delete=models.CASCADE, related_name='detalles')
    lote = models.ForeignKey(Lote, on_delete=models.PROTECT)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de Liquidación'
        verbose_name_plural = 'Detalles de Liquidación'
        unique_together = ['liquidacion', 'lote']
        
    def __str__(self):
        return f"Detalle - {self.lote.codigo_lote}"
        
    def save(self, *args, **kwargs):
        # Si no se especifica monto_pagado, usar el monto_pagar de la valorización
        if not self.monto_pagado:
            self.monto_pagado = self.lote.valorizacion.monto_pagar
        super().save(*args, **kwargs)
