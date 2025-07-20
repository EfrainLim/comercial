from django.contrib import admin
from .models import Liquidacion, LiquidacionDetalle
from lotes.models import Lote

@admin.register(Liquidacion)
class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_inicio', 'fecha_fin', 'estado', 'monto_total', 'fecha_creacion')
    list_filter = ('estado', 'proveedor')
    search_fields = ('id', 'proveedor__razon_social', 'proveedor__ruc')
    date_hierarchy = 'fecha_creacion'

@admin.register(LiquidacionDetalle)
class LiquidacionDetalleAdmin(admin.ModelAdmin):
    list_display = ('liquidacion', 'lote', 'monto_pagado')
    search_fields = ('liquidacion__id', 'lote__codigo_lote')

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('codigo_lote', 'fecha_ingreso', 'facturador', 'codigo_ingemmet', 'tipo_producto', 'tmh', 'estado')
    list_filter = ('estado', 'facturador', 'tipo_producto')
    search_fields = ('codigo_lote', 'facturador__razon_social', 'codigo_ingemmet__codigo_ingemmet')
