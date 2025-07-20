from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django_tables2 import RequestConfig
from .models import Ley
from .tables import LeyTable
from .forms import LeyForm
from .filters import LeyFilter
from usuarios.models import Usuario
from decimal import Decimal
from django.utils import timezone

# Create your views here.

@permission_required('laboratorio.view_ley', raise_exception=True)
def ley_list(request):
    # Obtener filtros
    f = LeyFilter(request.GET, queryset=Ley.objects.all().order_by('-fecha_creacion'))
    
    # Crear tabla
    table = LeyTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'laboratorio/ley_list.html', context)

@permission_required('laboratorio.add_ley', raise_exception=True)
def ley_create(request):
    if request.method == 'POST':
        form = LeyForm(request.POST)
        if form.is_valid():
            ley = form.save(commit=False)
            usuario = Usuario.objects.get(username=request.user.username)
            ley.usuario_creador = usuario
            
            # Calcular TMS
            tmh = ley.lote.tmh
            ley.tms = tmh - (tmh * (ley.porcentaje_h2o / Decimal('100')))
            
            ley.save()
            messages.success(request, 'Ley creada correctamente.')
            return redirect('laboratorio:ley_detail', pk=ley.pk)
    else:
        form = LeyForm()
    
    context = {
        'form': form,
        'title': 'Nueva Ley',
    }
    return render(request, 'laboratorio/ley_form.html', context)

@permission_required('laboratorio.view_ley', raise_exception=True)
def ley_detail(request, pk):
    ley = get_object_or_404(Ley, pk=pk)
    context = {
        'ley': ley,
    }
    return render(request, 'laboratorio/ley_detail.html', context)

@permission_required('laboratorio.change_ley', raise_exception=True)
@login_required
def ley_update(request, pk):
    ley = get_object_or_404(Ley, pk=pk)
    
    if ley.lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede editar la ley de un lote que ya está liquidado.')
        return redirect('laboratorio:ley_list')
    
    if request.method == 'POST':
        form = LeyForm(request.POST, instance=ley)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ley actualizada correctamente.')
            return redirect('laboratorio:ley_list')
    else:
        form = LeyForm(instance=ley)
    
    return render(request, 'laboratorio/ley_form.html', {'form': form})

@permission_required('laboratorio.delete_ley', raise_exception=True)
@login_required
def ley_delete(request, pk):
    ley = get_object_or_404(Ley, pk=pk)
    
    if ley.lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede eliminar la ley de un lote que ya está liquidado.')
        return redirect('laboratorio:ley_list')
    
    if hasattr(ley.lote, 'costo') or hasattr(ley.lote, 'valorizacion'):
        messages.error(request, 'No se puede eliminar una ley que ya tiene costo o valorización.')
        return redirect('laboratorio:ley_list')
    
    if request.method == 'POST':
        ley.delete()
        messages.success(request, 'Ley eliminada correctamente.')
        return redirect('laboratorio:ley_list')
    
    return render(request, 'laboratorio/ley_confirm_delete.html', {'ley': ley})
