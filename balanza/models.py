from django.db import models
from django.utils import timezone
from entidades.models import Facturador, Vehiculo, Conductor, TipoProducto
from usuarios.models import Usuario
from django.db.models import Max
import pytz
from django.utils.functional import cached_property

class Balanza(models.Model):
    numero_guia_ticket = models.CharField(max_length=20, unique=True)
    facturador = models.ForeignKey(Facturador, on_delete=models.PROTECT)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT)
    lote_temporal = models.CharField(max_length=50, blank=True, null=True)
    guia_remision = models.CharField(max_length=50, blank=True, null=True)
    guia_transporte = models.CharField(max_length=50, blank=True, null=True)
    peso_ingreso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    peso_salida_kg = models.DecimalField(max_digits=10, decimal_places=2)
    peso_neto_kg = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registro de Balanza'
        verbose_name_plural = 'Registros de Balanza'
        
    def __str__(self):
        return f"{self.numero_guia_ticket} - {self.facturador.razon_social}"

    @cached_property
    def fecha_creacion_local(self):
        lima_tz = pytz.timezone('America/Lima')
        return self.fecha_creacion.astimezone(lima_tz)

    @cached_property
    def fecha_actualizacion_local(self):
        lima_tz = pytz.timezone('America/Lima')
        return self.fecha_actualizacion.astimezone(lima_tz)
        
    def save(self, *args, **kwargs):
        # Calcular peso neto
        self.peso_neto_kg = self.peso_ingreso_kg - self.peso_salida_kg
        
        # Validar campos obligatorios para productos minerales
        if self.tipo_producto.es_mineral and not self.lote_temporal:
            raise ValueError("El campo lote_temporal es obligatorio para productos minerales")
        
        # Validar campos obligatorios para MASBP y MAMSP
        if self.tipo_producto.nombre in ['MASBP', 'MAMSP']:
            if not all([self.lote_temporal, self.guia_remision, self.guia_transporte]):
                raise ValueError("Los campos lote_temporal, guia_remision y guia_transporte son obligatorios para MASBP y MAMSP")
        
        # Generar numero_guia_ticket si no existe
        if not self.numero_guia_ticket:
            # Obtener la hora actual en la zona horaria de Perú
            lima_tz = pytz.timezone('America/Lima')
            fecha_actual = timezone.now().astimezone(lima_tz)
            
            # Obtener el último número de guía del día
            ultimo_numero = Balanza.objects.filter(
                fecha_creacion__date=fecha_actual.date()
            ).aggregate(Max('numero_guia_ticket'))['numero_guia_ticket__max']
            
            if ultimo_numero:
                try:
                    # Extraer el número y aumentarlo en 1
                    numero = int(ultimo_numero.split('-')[-1]) + 1
                except (ValueError, IndexError):
                    # Si hay algún error al extraer el número, empezar con 1
                    numero = 1
            else:
                # Si no hay registros hoy, empezar con 1
                numero = 1
            
            # Formatear el número con ceros a la izquierda (4 dígitos)
            self.numero_guia_ticket = f"{fecha_actual.strftime('%Y%m%d')}-{numero:04d}"
        
        super().save(*args, **kwargs)
