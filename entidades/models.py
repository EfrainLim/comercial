from django.db import models
from django.utils import timezone

# Create your models here.

class Facturador(models.Model):
    TIPOS = (
        ('empresa', 'Empresa'),
        ('acopio', 'Acopio'),
        ('contrata', 'Contrata'),
        ('sociedad', 'Sociedad'),
        ('transportista', 'Transportista'),
        ('otro', 'Otro'),
    )
    BANCOS = (
        ('bcp', 'BCP'),
        ('bbva', 'BBVA'),
        ('interbank', 'Interbank'),
        ('scotiabank', 'Scotiabank'),
        ('nacion', 'Nación'),
        ('pichincha', 'Pichincha'),
        ('mibanco', 'Mibanco'),
        ('creditea', 'Creditea'),
        ('banbif', 'BanBif'),
        ('falabella', 'Falabella'),
        ('azteca', 'Azteca'),
        ('gnb', 'GNB'),
        ('otro', 'Otro'),
    )
    
    razon_social = models.CharField(max_length=200)
    ruc = models.CharField(max_length=11, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    banco = models.CharField(max_length=50, choices=BANCOS, blank=True, null=True, verbose_name='Banco')
    numero_cuenta_bancaria = models.CharField(max_length=30, blank=True, null=True, verbose_name='Número de Cuenta Bancaria')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Facturador'
        verbose_name_plural = 'Facturadores'
        
    def __str__(self):
        return self.razon_social

class ProveedorIngemmet(models.Model):
    codigo_ingemmet = models.CharField(max_length=50, unique=True, verbose_name="Código INGEMMET")
    procedencia = models.CharField(max_length=100, verbose_name="Procedencia")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    
    class Meta:
        verbose_name = 'Código Ingemmet'
        verbose_name_plural = 'Códigos Ingemmet'
        
    def __str__(self):
        return f"{self.codigo_ingemmet} - {self.procedencia}"

class Vehiculo(models.Model):
    TIPOS = (
        ('camion', 'Camión'),
        ('volquete', 'Volquete'),
        ('otro', 'Otro'),
    )
    
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    facturador = models.ForeignKey(Facturador, on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        
    def __str__(self):
        return f"{self.placa} - {self.get_tipo_display()}"

class Conductor(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=200)
    licencia_conducir = models.CharField(max_length=20)
    categoria_licencia = models.CharField(max_length=10, blank=True, null=True)
    fecha_emision_licencia = models.DateField(blank=True, null=True)
    fecha_vencimiento_licencia = models.DateField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    empresa = models.CharField(max_length=200, blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'
        
    def __str__(self):
        return f"{self.nombres} - {self.dni}"
        
    def licencia_vencida(self):
        return self.fecha_vencimiento_licencia < timezone.now().date()

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    es_mineral = models.BooleanField(default=False, verbose_name="Es Mineral")
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tipo de Producto'
        verbose_name_plural = 'Tipos de Producto'
        
    def __str__(self):
        return self.nombre
