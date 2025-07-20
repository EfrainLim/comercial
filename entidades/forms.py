from django import forms
from .models import Facturador, Vehiculo, Conductor, ProveedorIngemmet, TipoProducto

class FacturadorForm(forms.ModelForm):
    class Meta:
        model = Facturador
        fields = [
            'razon_social',
            'ruc',
            'tipo',
            'direccion',
            'telefono',
            'correo',
            'observacion',
            'estado',
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'placa',
            'tipo',
            'facturador',
            'marca',
            'modelo',
            'observacion',
            'estado',
        ]
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'facturador': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = [
            'dni',
            'nombres',
            'licencia_conducir',
            'categoria_licencia',
            'fecha_emision_licencia',
            'fecha_vencimiento_licencia',
            'direccion',
            'empresa',
            'estado',
        ]
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'licencia_conducir': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria_licencia': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision_licencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento_licencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProveedorIngemmetForm(forms.ModelForm):
    class Meta:
        model = ProveedorIngemmet
        fields = [
            'codigo_ingemmet',
            'procedencia',
            'estado',
        ]
        widgets = {
            'codigo_ingemmet': forms.TextInput(attrs={'class': 'form-control'}),
            'procedencia': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre', 'descripcion', 'es_mineral', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'es_mineral': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        } 