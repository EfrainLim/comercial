from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django_tables2 import RequestConfig
from django.http import JsonResponse
from .models import Lote, Campana, CampanaLote
from .tables import LoteTable, CampanaTable
from .forms import LoteForm, CampanaForm, CampanaLoteForm, AgregarLotesACampanaForm
from .filters import LoteFilter, CampanaFilter

@login_required
@permission_required('lotes.view_lote', raise_exception=True)
def lote_list(request):
    # Obtener filtros
    f = LoteFilter(request.GET, queryset=Lote.objects.all().order_by('-fecha_creacion'))
    
    # Crear tabla
    table = LoteTable(f.qs)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'lotes/lote_list.html', context)

@login_required
@permission_required('lotes.add_lote', raise_exception=True)
def lote_create(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.usuario_creador = request.user
            lote.save()
            messages.success(request, 'Lote creado correctamente.')
            return redirect('lotes:lote_detail', pk=lote.pk)
    else:
        form = LoteForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Lote',
    }
    return render(request, 'lotes/lote_form.html', context)

@login_required
@permission_required('lotes.view_lote', raise_exception=True)
def lote_detail(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    context = {
        'lote': lote,
    }
    return render(request, 'lotes/lote_detail.html', context)

@login_required
@permission_required('lotes.change_lote', raise_exception=True)
def lote_update(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    
    if request.method == 'POST':
        form = LoteForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lote actualizado correctamente.')
            return redirect('lotes:lote_detail', pk=lote.pk)
    else:
        form = LoteForm(instance=lote)
    
    context = {
        'form': form,
        'title': 'Editar Lote',
        'lote': lote,
    }
    return render(request, 'lotes/lote_form.html', context)

@login_required
@permission_required('lotes.delete_lote', raise_exception=True)
def lote_delete(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    
    if lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede eliminar un lote que ya está liquidado.')
        return redirect('lotes:lote_list')
    
    if hasattr(lote, 'costo') or hasattr(lote, 'valorizacion') or hasattr(lote, 'ley'):
        messages.error(request, 'No se puede eliminar un lote que ya tiene ley, costo o valorización.')
        return redirect('lotes:lote_list')
    
    if request.method == 'POST':
        lote.delete()
        messages.success(request, 'Lote eliminado correctamente.')
        return redirect('lotes:lote_list')
    
    return render(request, 'lotes/lote_confirm_delete.html', {'lote': lote})

@login_required
def obtener_siguiente_codigo(request, codigo_sistema):
    # Obtener el último número de lote para el código sistema
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
    codigo_lote = f"{codigo_sistema}-{nuevo_numero:04d}"
    
    return JsonResponse({'codigo_lote': codigo_lote})

@login_required
@permission_required('lotes.view_campana', raise_exception=True)
def campana_list(request):
    f = CampanaFilter(request.GET, queryset=Campana.objects.all().order_by('-fecha_inicio'))
    table = CampanaTable(f.qs)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'lotes/campana_list.html', {'table': table, 'filter': f})

@login_required
@permission_required('lotes.add_campana', raise_exception=True)
def campana_create(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        if form.is_valid():
            campana = form.save(commit=False)
            campana.usuario_creador = request.user
            campana.save()
            messages.success(request, 'Campaña creada correctamente.')
            return redirect('lotes:campana_list')
    else:
        form = CampanaForm()
    return render(request, 'lotes/campana_form.html', {'form': form})

@login_required
@permission_required('lotes.change_campana', raise_exception=True)
def campana_update(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    if request.method == 'POST':
        form = CampanaForm(request.POST, instance=campana)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaña actualizada correctamente.')
            return redirect('lotes:campana_list')
    else:
        form = CampanaForm(instance=campana)
    return render(request, 'lotes/campana_form.html', {'form': form})

@login_required
@permission_required('lotes.delete_campana', raise_exception=True)
def campana_delete(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    if request.method == 'POST':
        campana.delete()
        messages.success(request, 'Campaña eliminada correctamente.')
        return redirect('lotes:campana_list')
    return render(request, 'lotes/campana_confirm_delete.html', {'campana': campana})

@login_required
@permission_required('lotes.add_campanalote', raise_exception=True)
def lote_add_to_campana(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method == 'POST':
        form = CampanaLoteForm(request.POST)
        if form.is_valid():
            campana = form.cleaned_data['campana']
            # Evitar duplicados
            if not CampanaLote.objects.filter(lote=lote, campana=campana).exists():
                CampanaLote.objects.create(lote=lote, campana=campana)
                messages.success(request, 'Lote agregado a la campaña correctamente.')
            else:
                messages.warning(request, 'El lote ya pertenece a esta campaña.')
            return redirect('lotes:lote_detail', pk=lote.pk)
    else:
        form = CampanaLoteForm()
    return render(request, 'lotes/lote_add_to_campana.html', {'form': form, 'lote': lote})

@login_required
@permission_required('lotes.view_campana', raise_exception=True)
def campana_detail(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    lotes = Lote.objects.filter(campanalote__campana=campana).select_related('costo')
    
    # Calcular totales
    total_tmh = sum(lote.tmh or 0 for lote in lotes)
    total_tms = sum(lote.costo.tms_real or 0 for lote in lotes)
    
    context = {
        'campana': campana,
        'lotes': lotes,
        'total_tmh': total_tmh,
        'total_tms': total_tms,
    }
    return render(request, 'lotes/campana_detail.html', context)

@login_required
@permission_required('lotes.add_campanalote', raise_exception=True)
def campana_agregar_lotes(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    if request.method == 'POST':
        form = AgregarLotesACampanaForm(request.POST)
        if form.is_valid():
            lotes = form.cleaned_data['lotes']
            for lote in lotes:
                CampanaLote.objects.get_or_create(campana=campana, lote=lote)
            messages.success(request, 'Lotes agregados correctamente a la campaña.')
            return redirect('lotes:campana_detail', pk=campana.pk)
    else:
        form = AgregarLotesACampanaForm()
    return render(request, 'lotes/campana_agregar_lotes.html', {'form': form, 'campana': campana})

@login_required
@permission_required('lotes.delete_campanalote', raise_exception=True)
def campana_quitar_lote(request, campana_pk, lote_pk):
    campana = get_object_or_404(Campana, pk=campana_pk)
    lote = get_object_or_404(Lote, pk=lote_pk)
    rel = get_object_or_404(CampanaLote, campana=campana, lote=lote)
    if request.method == 'POST':
        rel.delete()
        messages.success(request, 'Lote quitado de la campaña.')
        return redirect('lotes:campana_detail', pk=campana.pk)
    return render(request, 'lotes/campana_quitar_lote_confirm.html', {'campana': campana, 'lote': lote})

@login_required
@permission_required('lotes.change_campana', raise_exception=True)
def campana_finalizar(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    if campana.estado != 'activa':
        messages.warning(request, 'Solo se pueden finalizar campañas activas.')
        return redirect('lotes:campana_detail', pk=campana.pk)
    if request.method == 'POST':
        campana.estado = 'cerrada'
        campana.save()
        messages.success(request, 'La campaña ha sido finalizada correctamente.')
        return redirect('lotes:campana_detail', pk=campana.pk)
    return render(request, 'lotes/campana_finalizar_confirm.html', {'campana': campana})
