from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.management import call_command
from django.http import JsonResponse, FileResponse
from django.conf import settings
from .forms import UsuarioForm
from lotes.models import Lote
from laboratorio.models import Ley
from costos.models import Costo
from valorizacion.models import Valorizacion
from liquidaciones.models import Liquidacion
from django.db import models
from datetime import datetime
import os
import shutil
import tempfile

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
@permission_required('usuarios.can_backup_database', raise_exception=True)
def backup_database(request):
    """Vista para generar y descargar backup de la base de datos SQLite"""
    if request.method == 'POST':
        try:
            # Verificar que es SQLite
            db_engine = settings.DATABASES['default']['ENGINE']
            if 'sqlite' not in db_engine.lower():
                return JsonResponse({
                    'success': False,
                    'message': 'Este sistema solo funciona con SQLite'
                })
            
            # Obtener ruta de la base de datos
            db_path = settings.DATABASES['default']['NAME']
            if not os.path.exists(db_path):
                return JsonResponse({
                    'success': False,
                    'message': 'No se encontró la base de datos'
                })
            
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"sqlite_backup_{timestamp}.db"
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_file:
                temp_path = temp_file.name
                
                # Copiar archivo SQLite
                shutil.copy2(db_path, temp_path)
                
                # Obtener tamaño del archivo
                file_size = os.path.getsize(temp_path)
                size_mb = file_size / (1024 * 1024)
                
                # Crear respuesta de descarga
                response = FileResponse(
                    open(temp_path, 'rb'),
                    content_type='application/x-sqlite3'
                )
                response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
                response['Content-Length'] = file_size
                
                # Limpiar archivo temporal después de la respuesta
                def cleanup_temp_file():
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                
                response._handler_class = type('ResponseHandler', (), {
                    'close': lambda self: cleanup_temp_file()
                })
                
                return response
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al generar backup: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@permission_required('usuarios.can_restore_database', raise_exception=True)
def restore_database(request):
    """Vista para restaurar base de datos desde archivo subido"""
    if request.method == 'POST':
        try:
            # Verificar que se subió un archivo
            if 'backup_file' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'message': 'No se seleccionó ningún archivo'
                })
            
            uploaded_file = request.FILES['backup_file']
            
            # Verificar que es un archivo .db
            if not uploaded_file.name.endswith('.db'):
                return JsonResponse({
                    'success': False,
                    'message': 'El archivo debe ser un archivo .db válido'
                })
            
            # Verificar que es SQLite
            db_engine = settings.DATABASES['default']['ENGINE']
            if 'sqlite' not in db_engine.lower():
                return JsonResponse({
                    'success': False,
                    'message': 'Este sistema solo funciona con SQLite'
                })
            
            # Obtener ruta de la base de datos
            db_path = settings.DATABASES['default']['NAME']
            
            # Crear archivo temporal para el backup actual
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_before_restore = f"backup_before_restore_{timestamp}.db"
            
            # Crear backup de la BD actual si existe
            if os.path.exists(db_path):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_backup:
                    shutil.copy2(db_path, temp_backup.name)
                    backup_temp_path = temp_backup.name
            else:
                backup_temp_path = None
            
            # Guardar archivo subido en temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_upload:
                for chunk in uploaded_file.chunks():
                    temp_upload.write(chunk)
                upload_temp_path = temp_upload.name
            
            # Restaurar la base de datos
            shutil.copy2(upload_temp_path, db_path)
            
            # Limpiar archivos temporales
            try:
                os.unlink(upload_temp_path)
                if backup_temp_path:
                    os.unlink(backup_temp_path)
            except:
                pass
            
            return JsonResponse({
                'success': True,
                'message': f'Base de datos restaurada exitosamente desde {uploaded_file.name}',
                'backup_created': backup_before_restore if backup_temp_path else None
            })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al restaurar: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def perfil(request):
    # Obtener estadísticas del usuario
    usuario = request.user
    
    # Verificar si el usuario tiene permiso de backup
    can_backup = usuario.has_perm('usuarios.can_backup_database')
    
    # Obtener información de backups existentes
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backups = []
    if os.path.exists(backup_dir):
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith('sqlite_backup_') and f.endswith('.db')]
        backup_files.sort(reverse=True)
        for file in backup_files[:5]:  # Solo mostrar los últimos 5
            file_path = os.path.join(backup_dir, file)
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)
            backups.append({
                'filename': file,
                'size_mb': f'{size_mb:.2f}',
                'date': file.replace('sqlite_backup_', '').replace('.db', '')
            })
    
    context = {
        'usuario': usuario,
        'can_backup': can_backup,
        'backups': backups
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
