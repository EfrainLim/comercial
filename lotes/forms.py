from django import forms
from .models import Lote, Campana, CampanaLote
from django.db.models import Max
from entidades.models import Facturador, Vehiculo, Conductor, ProveedorIngemmet, TipoProducto

class LoteForm(forms.ModelForm):
    CODIGO_SISTEMA_CHOICES = [
        ('1', '1-Producción propia'),
        ('2', '2-Regalías'),
        ('3', '3-Acopio'),
        ('5', '5-Descuento contratas'),
        ('7', '7-PAD'),
    ]

    codigo_sistema = forms.ChoiceField(
        choices=CODIGO_SISTEMA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Código sistema'
    )

    codigo_lote = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Se generará automáticamente al seleccionar el código sistema'
        }),
        required=True
    )

    fecha_ingreso = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=True
    )

    tmh = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'min': '0'
        })
    )

    class Meta:
        model = Lote
        fields = [
            'codigo_sistema',
            'codigo_lote',
            'fecha_ingreso',
            'facturador',
            'codigo_ingemmet',
            'tipo_producto',
            'tmh',
            'vehiculo',
            'conductor',
            'transportista',
            'guia_remision',
            'guia_transporte',
            'nro_sacos',
            'concesion',
            'observacion',
            'estado'
        ]
        widgets = {
            'facturador': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar facturador...',
                'style': 'width: 100%;'
            }),
            'codigo_ingemmet': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar código Ingemmet...',
                'style': 'width: 100%;'
            }),
            'tipo_producto': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar tipo de producto...',
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
            'transportista': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Buscar transportista...',
                'style': 'width: 100%;'
            }),
            'guia_remision': forms.TextInput(attrs={'class': 'form-control'}),
            'guia_transporte': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_sacos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese número de sacos o "A GRANEL"'}),
            'concesion': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Si es un nuevo registro
            # Establecer fechas por defecto
            from django.utils import timezone
            fecha_actual = timezone.now()
            self.initial['fecha_ingreso'] = fecha_actual.date()
        else:  # Si es una edición
            # Asegurar que la fecha de ingreso se muestre en el formato correcto
            if self.instance.fecha_ingreso:
                self.initial['fecha_ingreso'] = self.instance.fecha_ingreso.strftime('%Y-%m-%d')
        
        # Configurar el campo de facturador con datos mejorados
        facturador_field = self.fields['facturador']
        facturador_field.queryset = Facturador.objects.filter(estado=True)
        
        # Mejorar las opciones del select para mostrar razón social y RUC
        facturador_field.choices = [('', '---------')] + [
            (facturador.id, f"{facturador.razon_social} - {facturador.ruc}")
            for facturador in facturador_field.queryset
        ]
        
        # Configurar el campo de código Ingemmet con datos mejorados
        codigo_ingemmet_field = self.fields['codigo_ingemmet']
        codigo_ingemmet_field.queryset = ProveedorIngemmet.objects.filter(estado=True)
        
        # Mejorar las opciones del select para mostrar más información
        codigo_ingemmet_field.choices = [('', '---------')] + [
            (proveedor.id, f"{proveedor.codigo_ingemmet} - {proveedor.procedencia}")
            for proveedor in codigo_ingemmet_field.queryset
        ]
        
        # Configurar el campo de tipo de producto con datos mejorados
        tipo_producto_field = self.fields['tipo_producto']
        tipo_producto_field.queryset = TipoProducto.objects.filter(estado=True)
        
        # Mejorar las opciones del select para mostrar más información
        tipo_producto_field.choices = [('', '---------')] + [
            (tipo.id, f"{tipo.nombre} - {'Mineral' if tipo.es_mineral else 'No Mineral'}")
            for tipo in tipo_producto_field.queryset
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
            (conductor.id, f"{conductor.nombres} - {conductor.dni}")
            for conductor in conductor_field.queryset
        ]
        
        # Configurar el campo de transportista con datos mejorados
        transportista_field = self.fields['transportista']
        transportista_field.queryset = Facturador.objects.filter(estado=True)
        
        # Mejorar las opciones del select para mostrar razón social y RUC
        transportista_field.choices = [('', '---------')] + [
            (facturador.id, f"{facturador.razon_social} - {facturador.ruc}")
            for facturador in transportista_field.queryset
        ]

    def clean(self):
        cleaned_data = super().clean()
        codigo_sistema = cleaned_data.get('codigo_sistema')
        codigo_lote = cleaned_data.get('codigo_lote')
        
        if not self.instance.pk:  # Solo para nuevos registros
            if not codigo_lote:  # Si no se ingresó un código manualmente
                # Obtener el último número de lote para el código sistema seleccionado
                ultimo_lote = Lote.objects.filter(
                    codigo_lote__startswith=f"{codigo_sistema}-"
                ).order_by('-codigo_lote').first()
                
                if ultimo_lote:
                    # Extraer el número y aumentarlo en 1
                    ultimo_numero = int(ultimo_lote.codigo_lote.split('-')[1])
                    nuevo_numero = ultimo_numero + 1
                else:
                    nuevo_numero = 1
                
                # Generar el nuevo código de lote
                cleaned_data['codigo_lote'] = f"{codigo_sistema}-{nuevo_numero:04d}"
            else:
                # Validar que el código lote comience con el código sistema seleccionado
                if not codigo_lote.startswith(f"{codigo_sistema}-"):
                    self.add_error('codigo_lote', 'El código de lote debe comenzar con el código sistema seleccionado')
                # Validar que el código lote no exista
                if Lote.objects.filter(codigo_lote=codigo_lote).exists():
                    self.add_error('codigo_lote', 'Este código de lote ya existe')
        
        return cleaned_data

class CampanaForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre de Campaña', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: MAYO-1'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.fecha_inicio:
                self.initial['fecha_inicio'] = self.instance.fecha_inicio.strftime('%Y-%m-%d')
            if self.instance.fecha_fin:
                self.initial['fecha_fin'] = self.instance.fecha_fin.strftime('%Y-%m-%d')

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        qs = Campana.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una campaña con este nombre.')
        return nombre

    class Meta:
        model = Campana
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class CampanaLoteForm(forms.ModelForm):
    class Meta:
        model = CampanaLote
        fields = ['campana']
        widgets = {
            'campana': forms.Select(attrs={'class': 'form-control'}),
        }

class AgregarLotesACampanaForm(forms.Form):
    lotes = forms.ModelMultipleChoiceField(
        queryset=Lote.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 10}),
        label='Selecciona los lotes a agregar'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lotes'].queryset = Lote.objects.exclude(campanalote__isnull=False) 