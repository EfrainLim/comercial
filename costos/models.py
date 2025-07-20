from django.db import models
from django.utils import timezone
from lotes.models import Lote
from usuarios.models import Usuario
from decimal import Decimal

class Costo(models.Model):
    TIPOS_ANALISIS = (
        ('NW', 'NW'),
        ('RE', 'RE'),
        ('RNW', 'RNW'),
    )
    
    lote = models.OneToOneField(Lote, on_delete=models.CASCADE)
    pio_us_onza = models.DecimalField(max_digits=10, decimal_places=2)
    rc = models.DecimalField(max_digits=10, decimal_places=2)
    maquila = models.DecimalField(max_digits=10, decimal_places=2)
    consumo_adicional = models.DecimalField(max_digits=10, decimal_places=2)
    analisis_newmonth = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_analisis = models.CharField(max_length=3, choices=TIPOS_ANALISIS)
    analisis_usd = models.DecimalField(max_digits=10, decimal_places=2)
    precio_usd_tms = models.DecimalField(max_digits=10, decimal_places=2)
    humedad_lab = models.DecimalField(max_digits=5, decimal_places=2)
    tms_real = models.DecimalField(max_digits=10, decimal_places=3)
    ley_lab = models.DecimalField(max_digits=10, decimal_places=3)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Costo'
        verbose_name_plural = 'Costos'
        
    def __str__(self):
        return f"Costo - {self.lote.codigo_lote}"
        
    def save(self, *args, **kwargs):
        # Obtener datos de la ley
        ley = self.lote.ley
        tmh = self.lote.tmh
        
        # Calcular humedad_lab
        self.humedad_lab = round(ley.porcentaje_h2o / Decimal('1.2'), 2)
        
        # Calcular tms_real
        self.tms_real = round(tmh - (tmh * (self.humedad_lab / Decimal('100'))), 3)
        
        # Calcular ley_lab
        self.ley_lab = round(ley.ley_onz_tc / Decimal('0.95'), 3)
        
        # Convertir porcentaje de recuperación a decimal
        recuperacion_decimal = ley.porcentaje_recuperacion / Decimal('100')
        
        # Calcular precio_usd_tms
        self.precio_usd_tms = round(
            ((self.pio_us_onza - self.rc) * ley.ley_onz_tc * recuperacion_decimal - self.maquila - self.consumo_adicional) * Decimal('1.10231') - (self.analisis_newmonth / ley.tms), 2
        )
        
        # Actualizar fecha_costo_agregado en el lote
        self.lote.fecha_costo_agregado = timezone.now()
        self.lote.save()
        
        super().save(*args, **kwargs)
