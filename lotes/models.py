from django.db import models
from django.utils import timezone
from entidades.models import Facturador, Vehiculo, Conductor, ProveedorIngemmet, TipoProducto
from usuarios.models import Usuario

class Lote(models.Model):
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('cancelado', 'Cancelado'),
    )
    
    codigo_sistema = models.CharField(max_length=1, choices=[
        ('1', '1-Producción propia'),
        ('2', '2-Regalías'),
        ('3', '3-Acopio'),
        ('5', '5-Descuento contratas'),
        ('7', '7-PAD'),
    ])
    codigo_lote = models.CharField(max_length=20, unique=True)
    fecha_ingreso = models.DateField()
    facturador = models.ForeignKey(Facturador, on_delete=models.PROTECT)
    ruc = models.CharField(max_length=11)
    codigo_ingemmet = models.ForeignKey(ProveedorIngemmet, on_delete=models.PROTECT)
    procedencia = models.CharField(max_length=100)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT)
    tmh = models.DecimalField(max_digits=10, decimal_places=3)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT)
    transportista = models.ForeignKey(Facturador, on_delete=models.PROTECT, related_name='lotes_transportados')
    guia_remision = models.CharField(max_length=50)
    guia_transporte = models.CharField(max_length=50)
    nro_sacos = models.CharField(max_length=50, verbose_name='Nro sacos')
    concesion = models.CharField(max_length=100)
    observacion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    fecha_ley_agregada = models.DateTimeField(null=True, blank=True)
    fecha_costo_agregado = models.DateTimeField(null=True, blank=True)
    fecha_valorizacion_agregada = models.DateTimeField(null=True, blank=True)
    fecha_liquidacion_agregada = models.DateTimeField(null=True, blank=True)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='lotes_creados')
    usuario_modificador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='lotes_modificados', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        
    def __str__(self):
        return f"{self.codigo_lote} - {self.facturador.razon_social}"
        
    def save(self, *args, **kwargs):
        # Obtener RUC del facturador
        self.ruc = self.facturador.ruc
        
        # Obtener procedencia del código Ingemmet
        self.procedencia = self.codigo_ingemmet.procedencia
        
        super().save(*args, **kwargs)

class Campana(models.Model):
    ESTADOS = (
        ('activa', 'Activa'),
        ('cerrada', 'Cerrada'),
        ('anulada', 'Anulada'),
    )
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='campanas_creadas')
    usuario_modificador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='campanas_modificadas', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'
        
    def __str__(self):
        return self.nombre

class CampanaLote(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Lote en Campaña'
        verbose_name_plural = 'Lotes en Campañas'
        unique_together = ['campana', 'lote']
        
    def __str__(self):
        return f"{self.lote.codigo_lote} - {self.campana.nombre}"
