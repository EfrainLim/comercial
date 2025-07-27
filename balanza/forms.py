from django import forms
from django.utils import timezone
from django.db.models import Max
from .models import Balanza
from entidades.models import Vehiculo, Conductor, Facturador
from datetime import datetime
import pytz

class BalanzaForm(forms.ModelForm):
    class Meta:
        model = Balanza
        fields = [
            'numero_guia_ticket',
            'facturador',
            'vehiculo',
            'conductor',
            'tipo_producto',
            'lote_temporal',
            'guia_remision',
            'guia_transporte',
            'peso_ingreso_kg',
            'peso_salida_kg',
            'tipo_empaque',
            'cantidad_sacos',
            'observaciones',
            'fecha_ingreso',
            'hora_ingreso',
            'fecha_salida',
            'hora_salida',
        ]
        widgets = {
            'numero_guia_ticket': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'facturador': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar facturador...',
                'style': 'width: 100%;'
            }),
            'vehiculo': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar vehículo...',
                'style': 'width: 100%;'
            }),
            'conductor': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar conductor...',
                'style': 'width: 100%;'
            }),
            'tipo_producto': forms.Select(attrs={'class': 'form-control'}),
            'lote_temporal': forms.TextInput(attrs={'class': 'form-control'}),
            'guia_remision': forms.TextInput(attrs={'class': 'form-control'}),
            'guia_transporte': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_empaque': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_sacos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ingrese cantidad de sacos'
            }),
            'peso_ingreso_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ejemplo: 5000'
            }),
            'peso_salida_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ejemplo: 5000'
            }),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_ingreso': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'hora_ingreso': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'},
                format='%H:%M'
            ),
            'fecha_salida': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'hora_salida': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'},
                format='%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Si es un nuevo registro
            # Obtener la hora actual en la zona horaria de Perú
            lima_tz = pytz.timezone('America/Lima')
            fecha_actual = timezone.now().astimezone(lima_tz)
            fecha_str = fecha_actual.strftime('%Y%m%d')
            
            # Obtener todos los números de guía del día
            numeros_del_dia = Balanza.objects.filter(
                numero_guia_ticket__startswith=fecha_str
            ).values_list('numero_guia_ticket', flat=True)
            
            # Encontrar el siguiente número disponible
            numero = 1
            while True:
                numero_guia = f"{fecha_str}-{numero:04d}"
                if numero_guia not in numeros_del_dia:
                    break
                numero += 1
            
            # Establecer el número de guía
            self.initial['numero_guia_ticket'] = numero_guia
            
            # Establecer fechas y horas por defecto
            self.initial['fecha_ingreso'] = fecha_actual.date()
            self.initial['hora_ingreso'] = fecha_actual.strftime('%H:%M')
            self.initial['fecha_salida'] = fecha_actual.date()
            self.initial['hora_salida'] = fecha_actual.strftime('%H:%M')
        
        # Configurar el campo de facturador con datos mejorados
        facturador_field = self.fields['facturador']
        facturador_field.queryset = Facturador.objects.filter(estado=True)
        
        # Mejorar las opciones del select para mostrar razón social y RUC
        facturador_field.choices = [('', '---------')] + [
            (facturador.id, f"{facturador.razon_social} - {facturador.ruc}")
            for facturador in facturador_field.queryset
        ]
        
        # Configurar el campo de vehículo con datos mejorados
        vehiculo_field = self.fields['vehiculo']
        vehiculo_field.queryset = Vehiculo.objects.filter(estado=True).select_related('facturador')
        
        # Mejorar las opciones del select para mostrar más información
        vehiculo_field.choices = [('', '---------')] + [
            (vehiculo.id, f"{vehiculo.placa} - {vehiculo.get_tipo_display()} - {vehiculo.facturador.razon_social}")
            for vehiculo in vehiculo_field.queryset
        ]
        
        # Configurar el campo de conductor con datos mejorados
        conductor_field = self.fields['conductor']
        conductor_field.queryset = Conductor.objects.filter(estado=True)
        
        # Mejorar las opciones del select para mostrar más información
        conductor_field.choices = [('', '---------')] + [
            (conductor.id, f"{conductor.nombres} - {conductor.licencia_conducir}")
            for conductor in conductor_field.queryset
        ]
        
        # Agregar el atributo data-es-mineral a las opciones del select
        tipo_producto_field = self.fields['tipo_producto']
        tipo_producto_field.widget.attrs['class'] = 'form-control'
        
        # Crear un diccionario con los valores de es_mineral para cada tipo de producto
        self.tipo_producto_es_mineral = {
            choice.pk: choice.es_mineral
            for choice in tipo_producto_field.queryset
        }
        
        # Configurar el campo de tipo de empaque
        tipo_empaque_field = self.fields['tipo_empaque']
        tipo_empaque_field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        tipo_producto = cleaned_data.get('tipo_producto')
        lote_temporal = cleaned_data.get('lote_temporal')
        tipo_empaque = cleaned_data.get('tipo_empaque')
        cantidad_sacos = cleaned_data.get('cantidad_sacos')

        if tipo_producto and tipo_producto.es_mineral and not lote_temporal:
            self.add_error('lote_temporal', 'El campo lote temporal es obligatorio para productos minerales')

        # Validar campos de empaque para productos minerales
        if tipo_producto and tipo_producto.es_mineral:
            if not tipo_empaque:
                self.add_error('tipo_empaque', 'El campo tipo carga mineral es obligatorio para productos minerales')
            elif tipo_empaque == 'SACOS' and not cantidad_sacos:
                self.add_error('cantidad_sacos', 'El campo cantidad de sacos es obligatorio cuando el tipo carga mineral es SACOS')

        return cleaned_data 