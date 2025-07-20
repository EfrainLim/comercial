from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django_tables2 import RequestConfig
from .models import Facturador, Vehiculo, Conductor, ProveedorIngemmet, TipoProducto
from .tables import FacturadorTable, VehiculoTable, ConductorTable, ProveedorIngemmetTable, TipoProductoTable
from .forms import FacturadorForm, VehiculoForm, ConductorForm, ProveedorIngemmetForm, TipoProductoForm
from .filters import FacturadorFilter, VehiculoFilter, ConductorFilter, ProveedorIngemmetFilter
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Vistas para Facturador
@permission_required('entidades.view_facturador', raise_exception=True)
def facturador_list(request):
    f = FacturadorFilter(request.GET, queryset=Facturador.objects.all().order_by('-fecha_creacion'))
    table = FacturadorTable(f.qs)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'entidades/facturador_list.html', context)

@permission_required('entidades.add_facturador', raise_exception=True)
def facturador_create(request):
    if request.method == 'POST':
        form = FacturadorForm(request.POST)
        if form.is_valid():
            facturador = form.save(commit=False)
            facturador.usuario_registro = request.user
            facturador.save()
            messages.success(request, 'Facturador creado correctamente.')
            return redirect('entidades:facturador_detail', pk=facturador.pk)
    else:
        form = FacturadorForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Facturador',
    }
    return render(request, 'entidades/facturador_form.html', context)

@permission_required('entidades.view_facturador', raise_exception=True)
def facturador_detail(request, pk):
    facturador = get_object_or_404(Facturador, pk=pk)
    context = {
        'object': facturador,
    }
    return render(request, 'entidades/facturador_detail.html', context)

@permission_required('entidades.change_facturador', raise_exception=True)
@login_required
def facturador_update(request, pk):
    facturador = get_object_or_404(Facturador, pk=pk)
    
    if request.method == 'POST':
        form = FacturadorForm(request.POST, instance=facturador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Facturador actualizado correctamente.')
            return redirect('entidades:facturador_detail', pk=facturador.pk)
    else:
        form = FacturadorForm(instance=facturador)
    
    context = {
        'form': form,
        'title': 'Editar Facturador',
        'facturador': facturador,
    }
    return render(request, 'entidades/facturador_form.html', context)

@permission_required('entidades.delete_facturador', raise_exception=True)
@login_required
def facturador_delete(request, pk):
    facturador = get_object_or_404(Facturador, pk=pk)
    
    if request.method == 'POST':
        facturador.delete()
        messages.success(request, 'Facturador eliminado correctamente.')
        return redirect('entidades:facturador_list')
    
    context = {
        'object': facturador,
    }
    return render(request, 'entidades/facturador_confirm_delete.html', context)

# Vistas para Vehiculo
@permission_required('entidades.view_vehiculo', raise_exception=True)
def vehiculo_list(request):
    f = VehiculoFilter(request.GET, queryset=Vehiculo.objects.all().order_by('-fecha_creacion'))
    table = VehiculoTable(f.qs)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'entidades/vehiculo_list.html', context)

@permission_required('entidades.add_vehiculo', raise_exception=True)
def vehiculo_create(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario_registro = request.user
            vehiculo.save()
            messages.success(request, 'Vehículo creado correctamente.')
            return redirect('entidades:vehiculo_detail', pk=vehiculo.pk)
    else:
        form = VehiculoForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Vehículo',
    }
    return render(request, 'entidades/vehiculo_form.html', context)

@permission_required('entidades.view_vehiculo', raise_exception=True)
def vehiculo_detail(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    context = {
        'object': vehiculo,
    }
    return render(request, 'entidades/vehiculo_detail.html', context)

@permission_required('entidades.change_vehiculo', raise_exception=True)
@login_required
def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('entidades:vehiculo_detail', pk=vehiculo.pk)
    else:
        form = VehiculoForm(instance=vehiculo)
    
    context = {
        'form': form,
        'title': 'Editar Vehículo',
        'vehiculo': vehiculo,
    }
    return render(request, 'entidades/vehiculo_form.html', context)

@permission_required('entidades.delete_vehiculo', raise_exception=True)
@login_required
def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado correctamente.')
        return redirect('entidades:vehiculo_list')
    
    context = {
        'object': vehiculo,
    }
    return render(request, 'entidades/vehiculo_confirm_delete.html', context)

# Vistas para Conductor
@permission_required('entidades.view_conductor', raise_exception=True)
def conductor_list(request):
    f = ConductorFilter(request.GET, queryset=Conductor.objects.all().order_by('-fecha_creacion'))
    table = ConductorTable(f.qs)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'entidades/conductor_list.html', context)

@permission_required('entidades.add_conductor', raise_exception=True)
def conductor_create(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)
        if form.is_valid():
            conductor = form.save(commit=False)
            conductor.usuario_registro = request.user
            conductor.save()
            messages.success(request, 'Conductor creado correctamente.')
            return redirect('entidades:conductor_detail', pk=conductor.pk)
    else:
        form = ConductorForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Conductor',
    }
    return render(request, 'entidades/conductor_form.html', context)

@permission_required('entidades.view_conductor', raise_exception=True)
def conductor_detail(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)
    context = {
        'object': conductor,
    }
    return render(request, 'entidades/conductor_detail.html', context)

@permission_required('entidades.change_conductor', raise_exception=True)
@login_required
def conductor_update(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)
    
    if request.method == 'POST':
        form = ConductorForm(request.POST, instance=conductor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conductor actualizado correctamente.')
            return redirect('entidades:conductor_detail', pk=conductor.pk)
    else:
        form = ConductorForm(instance=conductor)
    
    context = {
        'form': form,
        'title': 'Editar Conductor',
        'conductor': conductor,
    }
    return render(request, 'entidades/conductor_form.html', context)

@permission_required('entidades.delete_conductor', raise_exception=True)
@login_required
def conductor_delete(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)
    
    if request.method == 'POST':
        conductor.delete()
        messages.success(request, 'Conductor eliminado correctamente.')
        return redirect('entidades:conductor_list')
    
    context = {
        'object': conductor,
    }
    return render(request, 'entidades/conductor_confirm_delete.html', context)

# Vistas para ProveedorIngemmet
@permission_required('entidades.view_proveedoringemmet', raise_exception=True)
def proveedor_ingemmet_list(request):
    f = ProveedorIngemmetFilter(request.GET, queryset=ProveedorIngemmet.objects.all().order_by('-id'))
    table = ProveedorIngemmetTable(f.qs)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'entidades/proveedor_ingemmet_list.html', context)

@permission_required('entidades.add_proveedoringemmet', raise_exception=True)
def proveedor_ingemmet_create(request):
    if request.method == 'POST':
        form = ProveedorIngemmetForm(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.usuario_registro = request.user
            proveedor.save()
            messages.success(request, 'Proveedor INGEMMET creado correctamente.')
            return redirect('entidades:proveedor_ingemmet_detail', pk=proveedor.pk)
    else:
        form = ProveedorIngemmetForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Proveedor INGEMMET',
    }
    return render(request, 'entidades/proveedor_ingemmet_form.html', context)

@permission_required('entidades.view_proveedoringemmet', raise_exception=True)
def proveedor_ingemmet_detail(request, pk):
    proveedor = get_object_or_404(ProveedorIngemmet, pk=pk)
    context = {
        'object': proveedor,
    }
    return render(request, 'entidades/proveedor_ingemmet_detail.html', context)

@permission_required('entidades.change_proveedoringemmet', raise_exception=True)
@login_required
def proveedor_ingemmet_update(request, pk):
    proveedor = get_object_or_404(ProveedorIngemmet, pk=pk)
    
    if request.method == 'POST':
        form = ProveedorIngemmetForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor INGEMMET actualizado correctamente.')
            return redirect('entidades:proveedor_ingemmet_detail', pk=proveedor.pk)
    else:
        form = ProveedorIngemmetForm(instance=proveedor)
    
    context = {
        'form': form,
        'title': 'Editar Proveedor INGEMMET',
        'proveedor': proveedor,
    }
    return render(request, 'entidades/proveedor_ingemmet_form.html', context)

@permission_required('entidades.delete_proveedoringemmet', raise_exception=True)
@login_required
def proveedor_ingemmet_delete(request, pk):
    proveedor = get_object_or_404(ProveedorIngemmet, pk=pk)
    
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor INGEMMET eliminado correctamente.')
        return redirect('entidades:proveedor_ingemmet_list')
    
    context = {
        'object': proveedor,
    }
    return render(request, 'entidades/proveedor_ingemmet_confirm_delete.html', context)

class TipoProductoListView(PermissionRequiredMixin, ListView):
    permission_required = 'entidades.view_tipoproducto'
    model = TipoProducto
    template_name = 'entidades/tipo_producto_list.html'
    context_object_name = 'tipos_producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = TipoProductoTable(TipoProducto.objects.all())
        RequestConfig(self.request, paginate={'per_page': 10}).configure(table)
        context['table'] = table
        return context

class TipoProductoCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'entidades.add_tipoproducto'
    model = TipoProducto
    form_class = TipoProductoForm
    template_name = 'entidades/tipo_producto_form.html'
    success_url = reverse_lazy('entidades:tipo_producto_list')

class TipoProductoUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'entidades.change_tipoproducto'
    model = TipoProducto
    form_class = TipoProductoForm
    template_name = 'entidades/tipo_producto_form.html'
    success_url = reverse_lazy('entidades:tipo_producto_list')

class TipoProductoDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'entidades.delete_tipoproducto'
    model = TipoProducto
    template_name = 'entidades/tipo_producto_confirm_delete.html'
    success_url = reverse_lazy('entidades:tipo_producto_list')
