from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import os
import shutil
from datetime import datetime

class Command(BaseCommand):
    help = 'Restaurar base de datos SQLite desde un archivo de backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--backup-file',
            type=str,
            required=True,
            help='Ruta del archivo de backup a restaurar',
        )
        parser.add_argument(
            '--create-backup-before-restore',
            action='store_true',
            help='Crear backup de la BD actual antes de restaurar',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 RESTAURANDO BASE DE DATOS")
        
        # Verificar que es SQLite
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'sqlite' not in db_engine.lower():
            self.stdout.write("❌ Este comando solo funciona con SQLite")
            return
        
        # Obtener ruta de la base de datos
        db_path = settings.DATABASES['default']['NAME']
        backup_file = options['backup_file']
        
        # Verificar que el archivo de backup existe
        if not os.path.exists(backup_file):
            self.stdout.write(f"❌ No se encontró el archivo de backup: {backup_file}")
            return
        
        # Verificar que es un archivo SQLite válido
        if not backup_file.endswith('.db'):
            self.stdout.write("❌ El archivo debe ser un archivo .db válido")
            return
        
        try:
            # Crear backup de la BD actual si se solicita
            if options['create_backup_before_restore']:
                self.stdout.write("📦 Creando backup de la BD actual antes de restaurar...")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_before_restore = f"backup_before_restore_{timestamp}.db"
                backup_path = os.path.join(settings.BASE_DIR, backup_before_restore)
                
                if os.path.exists(db_path):
                    shutil.copy2(db_path, backup_path)
                    self.stdout.write(f"✅ Backup creado: {backup_before_restore}")
                else:
                    self.stdout.write("⚠️ No se pudo crear backup de la BD actual (no existe)")
            
            # Crear backup del archivo actual si existe
            if os.path.exists(db_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_current = f"backup_current_{timestamp}.db"
                backup_current_path = os.path.join(settings.BASE_DIR, backup_current)
                shutil.copy2(db_path, backup_current_path)
                self.stdout.write(f"✅ Backup de BD actual: {backup_current}")
            
            # Restaurar la base de datos
            self.stdout.write(f"🔄 Restaurando desde: {backup_file}")
            shutil.copy2(backup_file, db_path)
            
            # Verificar que la restauración fue exitosa
            if os.path.exists(db_path):
                file_size = os.path.getsize(db_path)
                size_mb = file_size / (1024 * 1024)
                
                self.stdout.write(f"\n✅ RESTAURACIÓN COMPLETADA EXITOSAMENTE")
                self.stdout.write(f"📦 Archivo restaurado: {db_path}")
                self.stdout.write(f"📏 Tamaño: {size_mb:.2f} MB")
                self.stdout.write(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.stdout.write(f"🗄️ Backup original: {backup_file}")
                
                self.stdout.write(f"\n⚠️ IMPORTANTE:")
                self.stdout.write(f"   - Reinicia el servidor Django para aplicar los cambios")
                self.stdout.write(f"   - Verifica que la aplicación funcione correctamente")
                self.stdout.write(f"   - Los datos actuales han sido reemplazados")
                
            else:
                self.stdout.write("❌ Error: No se pudo restaurar la base de datos")
                
        except Exception as e:
            self.stdout.write(f"❌ ERROR durante la restauración: {e}")
            raise 