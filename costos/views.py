from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django_tables2 import SingleTableView, RequestConfig
from django_filters.views import FilterView
from .models import Costo
from .forms import CostoForm
from .tables import CostoTable
from .filters import CostoFilter

class CostoListView(LoginRequiredMixin, SingleTableView, FilterView):
    model = Costo
    table_class = CostoTable
    template_name = 'costos/costo_list.html'
    filterset_class = CostoFilter
    context_object_name = 'costos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filterset(self.filterset_class)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

class CostoCreateView(LoginRequiredMixin, CreateView):
    model = Costo
    form_class = CostoForm
    template_name = 'costos/costo_form.html'
    success_url = reverse_lazy('costos:costo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Costo'
        return context

    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        messages.success(self.request, 'Costo creado exitosamente.')
        return super().form_valid(form)

class CostoUpdateView(LoginRequiredMixin, UpdateView):
    model = Costo
    form_class = CostoForm
    template_name = 'costos/costo_form.html'
    success_url = reverse_lazy('costos:costo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Costo'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Costo actualizado exitosamente.')
        return super().form_valid(form)

class CostoDetailView(LoginRequiredMixin, DetailView):
    model = Costo
    template_name = 'costos/costo_detail.html'
    context_object_name = 'costo'

class CostoDeleteView(LoginRequiredMixin, DeleteView):
    model = Costo
    template_name = 'costos/costo_confirm_delete.html'
    success_url = reverse_lazy('costos:costo_list')
    context_object_name = 'costo'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Costo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@permission_required('costos.view_costo', raise_exception=True)
def costo_list(request):
    # Obtener filtros
    f = CostoFilter(request.GET, queryset=Costo.objects.all().order_by('-fecha_creacion'))
    
    # Crear tabla con paginación
    table = CostoTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'costos/costo_list.html', context)

@permission_required('costos.add_costo', raise_exception=True)
def costo_create(request):
    view = CostoCreateView.as_view()
    return view(request)

@permission_required('costos.change_costo', raise_exception=True)
@login_required
def costo_update(request, pk):
    costo = get_object_or_404(Costo, pk=pk)
    
    if costo.lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede editar el costo de un lote que ya está liquidado.')
        return redirect('costos:costo_list')
    
    if request.method == 'POST':
        form = CostoForm(request.POST, instance=costo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Costo actualizado correctamente.')
            return redirect('costos:costo_list')
    else:
        form = CostoForm(instance=costo)
    
    return render(request, 'costos/costo_form.html', {'form': form})

@permission_required('costos.view_costo', raise_exception=True)
def costo_detail(request, pk):
    view = CostoDetailView.as_view()
    return view(request, pk=pk)

@permission_required('costos.delete_costo', raise_exception=True)
@login_required
def costo_delete(request, pk):
    costo = get_object_or_404(Costo, pk=pk)
    
    if costo.lote.fecha_liquidacion_agregada:
        messages.error(request, 'No se puede eliminar el costo de un lote que ya está liquidado.')
        return redirect('costos:costo_list')
    
    if hasattr(costo.lote, 'valorizacion'):
        messages.error(request, 'No se puede eliminar un costo que ya tiene valorización.')
        return redirect('costos:costo_list')
    
    if request.method == 'POST':
        costo.delete()
        messages.success(request, 'Costo eliminado correctamente.')
        return redirect('costos:costo_list')
    
    return render(request, 'costos/costo_confirm_delete.html', {'costo': costo})
