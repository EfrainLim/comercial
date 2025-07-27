from django.core.management.base import BaseCommand
from entidades.models import Conductor

class Command(BaseCommand):
    help = 'Verificar la importación de conductores'

    def handle(self, *args, **options):
        total = Conductor.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 ESTADÍSTICAS DE CONDUCTORES:\n'
                f'   📋 Total conductores: {total}'
            )
        )
        
        self.stdout.write('\n=== PRIMEROS 15 CONDUCTORES ===')
        for c in Conductor.objects.all()[:15]:
            self.stdout.write(f'{c.dni} | {c.nombres} | Licencia: {c.licencia_conducir}')
            
        if total > 15:
            self.stdout.write(f'\n... y {total - 15} conductores más')
            
        self.stdout.write('\n=== ÚLTIMOS 5 CONDUCTORES ===')
        for c in Conductor.objects.all().reverse()[:5]:
            self.stdout.write(f'{c.dni} | {c.nombres} | Licencia: {c.licencia_conducir}')
            
        # Mostrar estadísticas de categorías de licencia
        self.stdout.write('\n=== CATEGORÍAS DE LICENCIA ===')
        from django.db.models import Count
        categorias = Conductor.objects.values('categoria_licencia').annotate(count=Count('categoria_licencia'))
        for cat in categorias:
            self.stdout.write(f'{cat["categoria_licencia"]}: {cat["count"]} conductores') 