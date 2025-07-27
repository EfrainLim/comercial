from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import os
import shutil
from datetime import datetime

class Command(BaseCommand):
    help = 'Mostrar información de backup de la base de datos SQLite'

    def add_arguments(self, parser):
        parser.add_argument(
            '--info-only',
            action='store_true',
            help='Solo mostrar información sin crear archivos',
        )

    def handle(self, *args, **options):
        self.stdout.write("📊 INFORMACIÓN DE BACKUP DE SQLITE")
        
        # Verificar que es SQLite
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'sqlite' not in db_engine.lower():
            self.stdout.write("❌ Este comando solo funciona con SQLite")
            return
        
        # Obtener ruta de la base de datos
        db_path = settings.DATABASES['default']['NAME']
        if not os.path.exists(db_path):
            self.stdout.write(f"❌ No se encontró la base de datos: {db_path}")
            return
        
        # Obtener información del archivo
        file_size = os.path.getsize(db_path)
        size_mb = file_size / (1024 * 1024)
        last_modified = datetime.fromtimestamp(os.path.getmtime(db_path))
        
        self.stdout.write(f"\n📊 INFORMACIÓN DE LA BASE DE DATOS:")
        self.stdout.write(f"   📁 Archivo: {db_path}")
        self.stdout.write(f"   📏 Tamaño: {size_mb:.2f} MB")
        self.stdout.write(f"   📅 Última modificación: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"   🗄️ Motor: {db_engine}")
        
        self.stdout.write(f"\n📋 INSTRUCCIONES:")
        self.stdout.write(f"   1. Ir a http://127.0.0.1:8000/perfil/")
        self.stdout.write(f"   2. Hacer clic en 'Descargar Backup'")
        self.stdout.write(f"   3. El archivo se descargará directamente a tu computadora")
        self.stdout.write(f"   4. No se guardan archivos en el servidor")
        
        self.stdout.write(f"\n✅ INFORMACIÓN MOSTRADA")
        self.stdout.write(f"📋 Para descargar backup, usa la interfaz web") 