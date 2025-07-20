from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from balanza.models import Balanza
from lotes.models import Lote, Campana
# Si tienes app laboratorio y reportes, descomenta las siguientes líneas:
# from laboratorio.models import Ley
# from reportes.models import Reporte

class Command(BaseCommand):
    help = 'Crea los grupos y permisos para los diferentes roles de usuario'

    def handle(self, *args, **kwargs):
        grupos = {
            'planta': 'Usuarios de Planta',
            'laboratorio': 'Usuarios de Laboratorio',
            'comercial': 'Usuarios de Comercial',
            'administrador': 'Administradores del Sistema'
        }

        for codigo, nombre in grupos.items():
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{nombre}" creado exitosamente'))
            else:
                self.stdout.write(self.style.WARNING(f'El grupo "{nombre}" ya existe'))

        permisos = Permission.objects.all()

        # Permisos para Planta
        grupo_planta = Group.objects.get(name='Usuarios de Planta')
        permisos_planta = Permission.objects.filter(
            content_type__model__in=['balanza', 'lote', 'campana'],
            codename__regex=r'^(add|change|delete|view)_'  # todos los permisos CRUD
        )
        # Permiso para ver reportes si existe el modelo
        # try:
        #     content_type_reporte = ContentType.objects.get(model='reporte')
        #     permiso_ver_reporte = Permission.objects.get(content_type=content_type_reporte, codename='view_reporte')
        #     permisos_planta = list(permisos_planta) + [permiso_ver_reporte]
        # except ContentType.DoesNotExist:
        #     pass
        grupo_planta.permissions.set(permisos_planta)

        # Permisos para Laboratorio
        grupo_lab = Group.objects.get(name='Usuarios de Laboratorio')
        permisos_lab = Permission.objects.none()
        # try:
        #     content_type_ley = ContentType.objects.get(model='ley')
        #     permisos_lab = Permission.objects.filter(content_type=content_type_ley, codename__regex=r'^(add|change|delete|view)_ley')
        # except ContentType.DoesNotExist:
        #     pass
        grupo_lab.permissions.set(permisos_lab)

        # Permisos para Comercial (acceso a casi todo)
        grupo_comercial = Group.objects.get(name='Usuarios de Comercial')
        # Puede acceder a todos los permisos excepto los de admin
        permisos_comercial = permisos.exclude(content_type__app_label='admin')
        grupo_comercial.permissions.set(permisos_comercial)

        # Administrador: todos los permisos
        grupo_admin = Group.objects.get(name='Administradores del Sistema')
        grupo_admin.permissions.set(permisos)

        self.stdout.write(self.style.SUCCESS('Permisos asignados exitosamente')) 