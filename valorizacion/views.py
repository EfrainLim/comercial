from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django_tables2 import RequestConfig
from .models import Valorizacion
from .tables import ValorizacionTable
from .forms import ValorizacionForm
from .filters import ValorizacionFilter
from django.http import JsonResponse
from lotes.models import Lote

# Create your views here.

@permission_required('valorizacion.view_valorizacion', raise_exception=True)
def valorizacion_list(request):
    # Obtener filtros
    f = ValorizacionFilter(request.GET, queryset=Valorizacion.objects.all().order_by('-fecha_creacion'))
    
    # Crear tabla con paginación
    table = ValorizacionTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'valorizacion/valorizacion_list.html', context)

@permission_required('valorizacion.add_valorizacion', raise_exception=True)
def valorizacion_create(request):
    if request.method == 'POST':
        form = ValorizacionForm(request.POST)
        if form.is_valid():
            valorizacion = form.save(commit=False)
            valorizacion.usuario_creador = request.user
            valorizacion.save()
            messages.success(request, 'Valorización creada correctamente.')
            return redirect('valorizacion:valorizacion_detail', pk=valorizacion.pk)
    else:
        form = ValorizacionForm()
    
    context = {
        'form': form,
        'title': 'Nueva Valorización',
    }
    return render(request, 'valorizacion/valorizacion_form.html', context)

@permission_required('valorizacion.view_valorizacion', raise_exception=True)
def valorizacion_detail(request, pk):
    valorizacion = get_object_or_404(Valorizacion, pk=pk)
    context = {
        'valorizacion': valorizacion,
    }
    return render(request, 'valorizacion/valorizacion_detail.html', context)

@permission_required('valorizacion.change_valorizacion', raise_exception=True)
@login_required
def valorizacion_update(request, pk):
    valorizacion = get_object_or_404(Valorizacion, pk=pk)
    
    if valorizacion.lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede editar la valorización de un lote que ya está liquidado.')
        return redirect('valorizacion:valorizacion_list')
    
    if request.method == 'POST':
        form = ValorizacionForm(request.POST, instance=valorizacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Valorización actualizada correctamente.')
            return redirect('valorizacion:valorizacion_list')
    else:
        form = ValorizacionForm(instance=valorizacion)
    
    return render(request, 'valorizacion/valorizacion_form.html', {'form': form})

@permission_required('valorizacion.delete_valorizacion', raise_exception=True)
@login_required
def valorizacion_delete(request, pk):
    valorizacion = get_object_or_404(Valorizacion, pk=pk)
    
    if valorizacion.lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede eliminar la valorización de un lote que ya está liquidado.')
        return redirect('valorizacion:valorizacion_list')
    
    if request.method == 'POST':
        valorizacion.delete()
        messages.success(request, 'Valorización eliminada correctamente.')
        return redirect('valorizacion:valorizacion_list')
    
    return render(request, 'valorizacion/valorizacion_confirm_delete.html', {'valorizacion': valorizacion})

def get_facturador_banco_cuenta(request):
    lote_id = request.GET.get('lote_id')
    try:
        lote = Lote.objects.select_related('facturador').get(pk=lote_id)
        facturador = lote.facturador
        
        # Verificar si el facturador tiene datos bancarios
        tiene_banco = bool(facturador.banco)
        tiene_cuenta = bool(facturador.numero_cuenta_bancaria)
        
        return JsonResponse({
            'banco': facturador.banco or '',
            'cuenta': facturador.numero_cuenta_bancaria or '',
            'facturador_nombre': facturador.razon_social,
            'tiene_banco': tiene_banco,
            'tiene_cuenta': tiene_cuenta,
            'success': True
        })
    except Lote.DoesNotExist:
        return JsonResponse({
            'banco': '',
            'cuenta': '',
            'facturador_nombre': '',
            'tiene_banco': False,
            'tiene_cuenta': False,
            'success': False,
            'error': 'Lote no encontrado'
        })
    except Exception as e:
        return JsonResponse({
            'banco': '',
            'cuenta': '',
            'facturador_nombre': '',
            'tiene_banco': False,
            'tiene_cuenta': False,
            'success': False,
            'error': str(e)
        })
