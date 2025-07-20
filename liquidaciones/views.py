from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django_tables2 import RequestConfig
from .models import Liquidacion, LiquidacionDetalle
from .tables import LiquidacionTable
from .forms import LiquidacionForm, LiquidacionDetalleForm
from .filters import LiquidacionFilter
from lotes.models import Lote
from django.utils import timezone
from decimal import Decimal

# Create your views here.

@permission_required('liquidaciones.view_liquidacion', raise_exception=True)
def liquidacion_list(request):
    # Obtener filtros
    f = LiquidacionFilter(request.GET, queryset=Liquidacion.objects.all().order_by('-fecha_creacion'))
    
    # Crear tabla
    table = LiquidacionTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'liquidaciones/liquidacion_list.html', context)

@permission_required('liquidaciones.add_liquidacion', raise_exception=True)
def liquidacion_create(request):
    if request.method == 'POST':
        form = LiquidacionForm(request.POST)
        if form.is_valid():
            try:
                # Guardar la liquidación y crear los detalles automáticamente
                liquidacion = form.save(commit=True, user=request.user, request=request)
                
                # Obtener los lotes del proveedor en el rango de fechas
                lotes_proveedor = Lote.objects.filter(
                    estado='activo',
                    fecha_liquidacion_agregada__isnull=True,
                    facturador=liquidacion.proveedor,
                    fecha_ingreso__range=[liquidacion.fecha_inicio, liquidacion.fecha_fin]
                )
                
                # Contar lotes por cada condición
                total_lotes = lotes_proveedor.count()
                lotes_con_ley = lotes_proveedor.filter(fecha_ley_agregada__isnull=False).count()
                lotes_con_costo = lotes_proveedor.filter(fecha_costo_agregado__isnull=False).count()
                lotes_con_fecha_valorizacion = lotes_proveedor.filter(fecha_valorizacion_agregada__isnull=False).count()
                lotes_con_valorizacion = lotes_proveedor.filter(valorizacion__isnull=False).count()
                
                # Crear mensaje de resumen
                resumen = f"""
                <strong>Resumen de lotes para el proveedor {liquidacion.proveedor.razon_social} en el período {liquidacion.fecha_inicio.strftime('%d/%m/%Y')} - {liquidacion.fecha_fin.strftime('%d/%m/%Y')}:</strong><br>
                - Total de lotes activos sin liquidar: {total_lotes}<br>
                - Lotes con ley: {lotes_con_ley}<br>
                - Lotes con costo: {lotes_con_costo}<br>
                - Lotes con fecha de valorización: {lotes_con_fecha_valorizacion}<br>
                - Lotes con valorización asociada: {lotes_con_valorizacion}
                """
                messages.info(request, resumen)
                
                # Filtrar lotes aptos para liquidar
                lotes_aptos = lotes_proveedor.filter(
                    fecha_ley_agregada__isnull=False,
                    fecha_costo_agregado__isnull=False,
                    fecha_valorizacion_agregada__isnull=False,
                    valorizacion__isnull=False
                ).select_related('valorizacion')
                
                # Crear detalles para cada lote apto
                lotes_agregados = 0
                for lote in lotes_aptos:
                    try:
                        LiquidacionDetalle.objects.create(
                            liquidacion=liquidacion,
                            lote=lote,
                            monto_pagado=float(lote.valorizacion.monto_pagar)
                        )
                        lotes_agregados += 1
                        messages.success(request, f'Lote {lote.codigo_lote} agregado correctamente con monto S/ {lote.valorizacion.monto_pagar:,.2f}')
                    except Exception as e:
                        messages.error(request, f'Error al crear detalle para lote {lote.codigo_lote}: {str(e)}')
                
                if lotes_agregados > 0:
                    messages.success(request, f'Se agregaron {lotes_agregados} lotes a la liquidación.')
                else:
                    messages.warning(request, 'No se encontraron lotes aptos para liquidar en el período seleccionado.')
                    messages.info(request, 'Verifica que los lotes tengan: ley, costo y valorización asociada, y que estén dentro del rango de fechas.')
                
                return redirect('liquidaciones:liquidacion_detail', pk=liquidacion.pk)
            except Exception as e:
                messages.error(request, f'Error al crear la liquidación: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = LiquidacionForm()
    
    return render(request, 'liquidaciones/liquidacion_form.html', {'form': form})

@permission_required('liquidaciones.view_liquidacion', raise_exception=True)
def liquidacion_detail(request, pk):
    liquidacion = get_object_or_404(Liquidacion, pk=pk)
    detalles = LiquidacionDetalle.objects.filter(liquidacion=liquidacion)
    
    # Cálculo de totales
    subtotal = sum(detalle.lote.valorizacion.valorizacion_uds_tms or Decimal('0') for detalle in detalles)
    igv = subtotal * Decimal('0.18')
    total_valorizacion = subtotal + igv
    anticipo = sum(detalle.lote.valorizacion.anticipo or Decimal('0') for detalle in detalles)
    total_valorizacion_neto = total_valorizacion - anticipo
    detraccion = total_valorizacion_neto * Decimal('0.10')
    # Nuevo cálculo de descuento flete usando pu_tmh_flete
    descuento_flete = sum(
        (detalle.lote.tmh or Decimal('0')) * (getattr(detalle.lote.valorizacion, 'pu_tmh_flete', Decimal('0')) or Decimal('0'))
        for detalle in detalles
    )
    monto_pagado = total_valorizacion_neto - detraccion - descuento_flete
    
    context = {
        'liquidacion': liquidacion,
        'detalles': detalles,
        'subtotal': subtotal,
        'igv': igv,
        'total_valorizacion': total_valorizacion,
        'anticipo': anticipo,
        'total_valorizacion_neto': total_valorizacion_neto,
        'detraccion': detraccion,
        'descuento_flete': descuento_flete,
        'monto_pagado': monto_pagado,
    }
    
    return render(request, 'liquidaciones/liquidacion_detail.html', context)

@permission_required('liquidaciones.change_liquidacion', raise_exception=True)
@login_required
def liquidacion_update(request, pk):
    liquidacion = get_object_or_404(Liquidacion, pk=pk)
    
    if request.method == 'POST':
        form = LiquidacionForm(request.POST, instance=liquidacion)
        if form.is_valid():
            liquidacion = form.save(commit=True, user=request.user)
            messages.success(request, 'Liquidación actualizada correctamente.')
            return redirect('liquidaciones:liquidacion_detail', pk=liquidacion.pk)
    else:
        form = LiquidacionForm(instance=liquidacion)
    
    context = {
        'form': form,
        'title': 'Editar Liquidación',
        'liquidacion': liquidacion,
    }
    return render(request, 'liquidaciones/liquidacion_form.html', context)

@permission_required('liquidaciones.delete_liquidacion', raise_exception=True)
@login_required
def liquidacion_delete(request, pk):
    liquidacion = get_object_or_404(Liquidacion, pk=pk)
    
    if request.method == 'POST':
        liquidacion.delete()
        messages.success(request, 'Liquidación eliminada correctamente.')
        return redirect('liquidaciones:liquidacion_list')
    
    context = {
        'liquidacion': liquidacion,
    }
    return render(request, 'liquidaciones/liquidacion_confirm_delete.html', context)

@login_required
def liquidacion_finalizar(request, pk):
    liquidacion = get_object_or_404(Liquidacion, pk=pk)
    
    if request.method == 'POST':
        if liquidacion.estado == 'borrador':
            try:
                # Calcular el monto total usando los mismos cálculos que en el template
                detalles = liquidacion.detalles.all()
                subtotal = sum(detalle.lote.valorizacion.valorizacion_uds_tms or Decimal('0') for detalle in detalles)
                igv = subtotal * Decimal('0.18')
                total_valorizacion = subtotal + igv
                anticipo = sum(detalle.lote.valorizacion.anticipo or Decimal('0') for detalle in detalles)
                total_valorizacion_neto = total_valorizacion - anticipo
                detraccion = total_valorizacion_neto * Decimal('0.10')
                descuento_flete = sum(
                    (detalle.lote.tmh or Decimal('0')) * (getattr(detalle.lote.valorizacion, 'pu_tmh_flete', Decimal('0')) or Decimal('0'))
                    for detalle in detalles
                )
                monto_total = total_valorizacion_neto - detraccion - descuento_flete
                
                # Actualizar el estado y el monto total
                liquidacion.estado = 'finalizada'
                liquidacion.monto_total = monto_total
                liquidacion.save()
                
                # Actualizar la fecha de liquidación en los lotes
                for detalle in liquidacion.detalles.all():
                    detalle.lote.fecha_liquidacion_agregada = timezone.now()
                    detalle.lote.save()
                
                messages.success(request, 'Liquidación finalizada correctamente.')
            except Exception as e:
                messages.error(request, f'Error al finalizar la liquidación: {str(e)}')
        else:
            messages.error(request, 'Solo se pueden finalizar liquidaciones en estado borrador.')
        
        return redirect('liquidaciones:liquidacion_detail', pk=liquidacion.pk)
    
    context = {
        'liquidacion': liquidacion,
    }
    return render(request, 'liquidaciones/liquidacion_confirm_finalizar.html', context)

@login_required
def liquidacion_detalle_update(request, pk):
    detalle = get_object_or_404(LiquidacionDetalle, pk=pk)
    
    if request.method == 'POST' and detalle.liquidacion.estado == 'borrador':
        monto_pagado = request.POST.get('monto_pagado')
        if monto_pagado:
            detalle.monto_pagado = monto_pagado
            detalle.save()
            messages.success(request, 'Monto actualizado correctamente.')
        else:
            messages.error(request, 'El monto no puede estar vacío.')
    
    return redirect('liquidaciones:liquidacion_detail', pk=detalle.liquidacion.pk)

@login_required
def liquidacion_detalle_delete(request, pk):
    detalle = get_object_or_404(LiquidacionDetalle, pk=pk)
    
    if request.method == 'POST' and detalle.liquidacion.estado == 'borrador':
        detalle.delete()
        messages.success(request, 'Lote eliminado de la liquidación correctamente.')
    
    return redirect('liquidaciones:liquidacion_detail', pk=detalle.liquidacion.pk)
