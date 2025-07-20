from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UsuarioForm
from lotes.models import Lote
from laboratorio.models import Ley
from costos.models import Costo
from valorizacion.models import Valorizacion
from liquidaciones.models import Liquidacion
from django.db import models
from datetime import datetime

@login_required
def home(request):
    # Obtener estadísticas para el dashboard
    lotes_activos = Lote.objects.filter(estado='activo').count()
    pendientes_ley = Lote.objects.filter(estado='activo', ley__isnull=True).count()
    pendientes_liquidacion = Lote.objects.filter(estado='activo', liquidaciondetalle__isnull=True).count()
    
    # Obtener últimos lotes registrados
    ultimos_lotes = Lote.objects.select_related('facturador').order_by('-fecha_creacion')[:5]
    
    # Obtener actividades recientes
    actividades = []
    
    # Actividades de lotes
    for lote in Lote.objects.order_by('-fecha_creacion')[:10]:
        actividades.append({
            'titulo': f'Nuevo lote registrado: {lote.codigo_lote}',
            'fecha': lote.fecha_creacion,
            'descripcion': f'Facturador: {lote.facturador.razon_social}'
        })

    # Actividades de leyes
    for ley in Ley.objects.order_by('-fecha_creacion')[:10]:
        actividades.append({
            'titulo': f'Nueva ley registrada: {ley.lote.codigo_lote}',
            'fecha': ley.fecha_creacion,
            'descripcion': f'Ley: {ley.ley_onz_tc} oz/tc'
        })

    # Actividades de costos
    for costo in Costo.objects.order_by('-fecha_creacion')[:10]:
        actividades.append({
            'titulo': f'Nuevo costo registrado: {costo.lote.codigo_lote}',
            'fecha': costo.fecha_creacion,
            'descripcion': f'Precio USD/TMS: ${costo.precio_usd_tms:.2f}'
        })

    # Actividades de valorizaciones
    for valorizacion in Valorizacion.objects.order_by('-fecha_creacion')[:10]:
        actividades.append({
            'titulo': f'Nueva valorización: {valorizacion.lote.codigo_lote}',
            'fecha': valorizacion.fecha_creacion,
            'descripcion': f'Monto a pagar: S/. {valorizacion.monto_pagar:.2f}'
        })

    # Actividades de liquidaciones nuevas
    for liquidacion in Liquidacion.objects.order_by('-fecha_creacion')[:10]:
        actividades.append({
            'titulo': f'Nueva liquidación: {liquidacion.id}',
            'fecha': liquidacion.fecha_creacion,
            'descripcion': f'Proveedor: {liquidacion.proveedor.razon_social} | Estado: {liquidacion.get_estado_display()}'
        })

    # Actividades de modificaciones de liquidaciones
    for liquidacion in Liquidacion.objects.exclude(fecha_modificacion=models.F('fecha_creacion')).order_by('-fecha_modificacion')[:10]:
        if liquidacion.usuario_modificador:
            nombre_modificador = liquidacion.usuario_modificador.get_full_name() or liquidacion.usuario_modificador.username
        else:
            nombre_modificador = "-"
        actividades.append({
            'titulo': f'Liquidación modificada: {liquidacion.id}',
            'fecha': liquidacion.fecha_modificacion,
            'descripcion': f'Modificado por: {nombre_modificador} | Estado: {liquidacion.get_estado_display()}'
        })

    # Actividades de modificaciones de ley
    for ley in Ley.objects.exclude(fecha_modificacion=models.F('fecha_creacion')).order_by('-fecha_modificacion')[:10]:
        if ley.usuario_modificador:
            nombre_modificador = ley.usuario_modificador.get_full_name() or ley.usuario_modificador.username
        else:
            nombre_modificador = "-"
        actividades.append({
            'titulo': f'Lote de ley modificado: {ley.lote.codigo_lote}',
            'fecha': ley.fecha_modificacion,
            'descripcion': f'Modificado por: {nombre_modificador} | Ley: {ley.ley_onz_tc} oz/tc'
        })

    # Ordenar actividades por fecha (todas naive)
    actividades.sort(
        key=lambda x: (x['fecha'].replace(tzinfo=None) if x['fecha'] else datetime.min),
        reverse=True
    )
    actividades = actividades[:10]
    
    cantidad_liquidaciones = Lote.objects.filter(liquidaciondetalle__isnull=False).distinct().count()
    
    context = {
        'lotes_activos': lotes_activos,
        'pendientes_ley': pendientes_ley,
        'cantidad_liquidaciones': cantidad_liquidaciones,
        'pendientes_liquidacion': pendientes_liquidacion,
        'ultimos_lotes': ultimos_lotes,
        'actividades': actividades,
    }
    
    return render(request, 'usuarios/home.html', context)

@login_required
def perfil(request):
    # Obtener estadísticas del usuario
    lotes_creados = Lote.objects.filter(usuario_creador=request.user).count()
    leyes_creadas = Ley.objects.filter(usuario_creador=request.user).count()
    liquidaciones_creadas = Liquidacion.objects.filter(usuario_creador=request.user).count()

    context = {
        'lotes_creados': lotes_creados,
        'leyes_creadas': leyes_creadas,
        'liquidaciones_creadas': liquidaciones_creadas,
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = UsuarioForm(instance=request.user)
    
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/cambiar_password.html', {'form': form})
