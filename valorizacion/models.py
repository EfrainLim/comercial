from django.db import models
from django.utils import timezone
from lotes.models import Lote
from usuarios.models import Usuario
from decimal import Decimal

class Valorizacion(models.Model):
    lote = models.OneToOneField(Lote, on_delete=models.CASCADE)
    condicion = models.CharField(max_length=100)
    comprobante = models.CharField(max_length=100)
    factura_nro = models.CharField(max_length=50, blank=True, null=True)
    pu_tmh_flete = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    finos_comercial = models.DecimalField(max_digits=10, decimal_places=2)
    gramos_recuperados_comercial = models.DecimalField(max_digits=10, decimal_places=2)
    valorizacion_uds_tms = models.DecimalField(max_digits=10, decimal_places=2)
    reintegro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    neto_pagar_1 = models.DecimalField(max_digits=10, decimal_places=2)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    neto_pagar_2 = models.DecimalField(max_digits=10, decimal_places=2)
    detraccion = models.DecimalField(max_digits=10, decimal_places=2)
    flete = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    banco = models.CharField(max_length=100)
    cuenta = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Valorización'
        verbose_name_plural = 'Valorizaciones'
        
    def __str__(self):
        return f"Valorización - {self.lote.codigo_lote}"
        
    def save(self, *args, **kwargs):
        # Obtener datos del lote y costo
        lote = self.lote
        costo = lote.costo
        ley = lote.ley
        
        # Calcular finos_comercial
        self.finos_comercial = round(
            (ley.tms * ley.ley_onz_tc) * Decimal('31.1035') * Decimal('1.1023'), 2
        )
        
        # Calcular gramos_recuperados_comercial
        self.gramos_recuperados_comercial = round(self.finos_comercial * Decimal('0.9'), 2)
        
        # Calcular valorizacion_uds_tms
        self.valorizacion_uds_tms = round(costo.precio_usd_tms * ley.tms, 2)
        
        # Calcular IGV
        self.igv = round(self.valorizacion_uds_tms * Decimal('0.18'), 2)
        
        # Calcular neto_pagar_1
        self.neto_pagar_1 = self.valorizacion_uds_tms + (self.reintegro or Decimal('0')) + self.igv
        
        # Calcular neto_pagar_2
        self.neto_pagar_2 = self.neto_pagar_1 - (self.anticipo or Decimal('0'))
        
        # Calcular detraccion
        self.detraccion = round(self.neto_pagar_2 * Decimal('0.10'), 2)
        
        # Calcular flete
        self.flete = round(lote.tmh * (self.pu_tmh_flete or Decimal('0')), 2)
        
        # Calcular monto_pagar
        self.monto_pagar = self.neto_pagar_2 - self.detraccion - self.flete
        
        # Actualizar fecha_valorizacion_agregada en el lote
        self.lote.fecha_valorizacion_agregada = timezone.now()
        self.lote.save()
        
        super().save(*args, **kwargs)
