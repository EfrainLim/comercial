from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django_tables2 import RequestConfig
from .models import Balanza
from .tables import BalanzaTable
from .forms import BalanzaForm
from .filters import BalanzaFilter
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from lotes.models import Lote  # Importar el modelo Lote
import pytz
from django.utils import timezone

# Create your views here.

@login_required
@permission_required('balanza.view_balanza', raise_exception=True)
def balanza_list(request):
    # Obtener filtros
    f = BalanzaFilter(request.GET, queryset=Balanza.objects.all().order_by('-fecha_creacion'))
    
    # Crear tabla
    table = BalanzaTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    
    # Generar PDF para cada registro de balanza
    for balanza in f.qs:
        generar_pdf_balanza(request, balanza.id)  # Llama a la función de generación de PDF
    
    context = {
        'table': table,
        'filter': f,
    }
    return render(request, 'balanza/balanza_list.html', context)

@login_required
@permission_required('balanza.add_balanza', raise_exception=True)
def balanza_create(request):
    if request.method == 'POST':
        form = BalanzaForm(request.POST)
        if form.is_valid():
            balanza = form.save(commit=False)
            # Obtener el modelo de usuario correcto
            Usuario = get_user_model()
            usuario = Usuario.objects.get(username=request.user.username)
            balanza.usuario_registro = usuario
            
            # Asegurar que las fechas estén en la zona horaria de Perú
            lima_tz = pytz.timezone('America/Lima')
            balanza.fecha_creacion = timezone.now().astimezone(lima_tz)
            balanza.fecha_actualizacion = timezone.now().astimezone(lima_tz)
            
            balanza.save()
            messages.success(request, 'Registro de balanza creado correctamente.')
            return redirect('balanza:balanza_detail', pk=balanza.pk)
    else:
        form = BalanzaForm()
    
    # Crear diccionario de tipos de producto y sus valores es_mineral
    tipo_producto_es_mineral = {
        str(tipo.id): tipo.es_mineral
        for tipo in form.fields['tipo_producto'].queryset
    }
    
    context = {
        'form': form,
        'title': 'Nuevo Registro de Balanza',
        'tipo_producto_es_mineral': json.dumps(tipo_producto_es_mineral),
    }
    return render(request, 'balanza/balanza_form.html', context)

@login_required
@permission_required('balanza.view_balanza', raise_exception=True)
def balanza_detail(request, pk):
    balanza = get_object_or_404(Balanza, pk=pk)
    context = {
        'balanza': balanza,
    }
    return render(request, 'balanza/balanza_detail.html', context)

@login_required
@permission_required('balanza.change_balanza', raise_exception=True)
def balanza_update(request, pk):
    balanza = get_object_or_404(Balanza, pk=pk)
    
    if request.method == 'POST':
        form = BalanzaForm(request.POST, instance=balanza)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de balanza actualizado correctamente.')
            return redirect('balanza:balanza_detail', pk=balanza.pk)
    else:
        form = BalanzaForm(instance=balanza)
    
    # Crear diccionario de tipos de producto y sus valores es_mineral
    tipo_producto_es_mineral = {
        str(tipo.id): tipo.es_mineral
        for tipo in form.fields['tipo_producto'].queryset
    }
    
    context = {
        'form': form,
        'title': 'Editar Registro de Balanza',
        'balanza': balanza,
        'tipo_producto_es_mineral': json.dumps(tipo_producto_es_mineral),
    }
    return render(request, 'balanza/balanza_form.html', context)

@login_required
@permission_required('balanza.delete_balanza', raise_exception=True)
def balanza_delete(request, pk):
    balanza = get_object_or_404(Balanza, pk=pk)
    
    if request.method == 'POST':
        balanza.delete()
        messages.success(request, 'Registro de balanza eliminado correctamente.')
        return redirect('balanza:balanza_list')
    
    context = {
        'balanza': balanza,
    }
    return render(request, 'balanza/balanza_confirm_delete.html', context)

# Vista para obtener los lotes temporales de los últimos 50 registros de balanza para el autocomplete en el formulario de registro de Lote
def obtener_lotes_temporales(request):
    # Obtener todos los códigos de lote existentes
    codigos_lote_existentes = set(Lote.objects.values_list('codigo_lote', flat=True))

    registros = Balanza.objects.filter(
        lote_temporal__isnull=False
    ).exclude(
        lote_temporal=''
    ).exclude(
        lote_temporal__in=codigos_lote_existentes
    ).select_related(
        'facturador',
        'vehiculo',
        'conductor',
        'tipo_producto'
    ).order_by('-fecha_ingreso')[:50]  # Limitamos a los últimos 50 registros

    data = [{
        'lote_temporal': registro.lote_temporal,
        'facturador': str(registro.facturador),
        'facturador_id': registro.facturador.id,
        'vehiculo': str(registro.vehiculo),
        'vehiculo_id': registro.vehiculo.id,
        'conductor': str(registro.conductor),
        'conductor_id': registro.conductor.id,
        'tipo_producto': str(registro.tipo_producto),
        'tipo_producto_id': registro.tipo_producto.id,
        'guia_remision': registro.guia_remision,
        'guia_transporte': registro.guia_transporte,
        'peso_neto_kg': registro.peso_neto_kg,
        'observaciones': registro.observaciones,
        'fecha_ingreso': registro.fecha_ingreso.strftime('%Y-%m-%d') if registro.fecha_ingreso else None,
        'tipo_empaque': registro.tipo_empaque,
        'cantidad_sacos': registro.cantidad_sacos,
    } for registro in registros]

    return JsonResponse(data, safe=False)

def generar_pdf_balanza(request, balanza_id):
    balanza = get_object_or_404(Balanza, id=balanza_id)
    
    # Generar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_balanza_{balanza.id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Registro de Balanza")
    p.drawString(100, 730, f"ID: {balanza.id}")
    p.drawString(100, 710, f"Peso: {balanza.peso_neto_kg} kg")
    p.drawString(100, 690, f"Fecha: {balanza.fecha_ingreso}")
    p.showPage()
    p.save()
    
    return response
