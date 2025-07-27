from django.core.management.base import BaseCommand
from entidades.models import Conductor
from datetime import date

class Command(BaseCommand):
    help = 'Importar 36 conductores'

    def handle(self, *args, **options):
        # Datos de conductores
        conductores_data = [
            {'dni': '42325479', 'nombres': 'SUMIRE BARRIENTOS, CORNELIO', 'licencia': 'Z-42325479'},
            {'dni': '16176311', 'nombres': 'LLAULLIPOMA ROJAS MOISES', 'licencia': 'Q-16176311'},
            {'dni': '29568539', 'nombres': 'EMILIO PÍNEDO SALCEDO', 'licencia': 'H-29568539'},
            {'dni': '21577805', 'nombres': 'SOTO CORONADO JESUS RAUL', 'licencia': 'F-21577805'},
            {'dni': '46188707', 'nombres': 'HUAÑAHUI QUISPE EDGAR', 'licencia': 'H-46188707'},
            {'dni': '41971992', 'nombres': 'SANTO HALANOCCA LUCIO', 'licencia': 'H-41971992'},
            {'dni': '43622785', 'nombres': 'URUCHIRI FERNANDEZ ADRIAN', 'licencia': 'K-43622785'},
            {'dni': '48996660', 'nombres': 'BASHUALDO REYES EMERSON', 'licencia': 'P-48996660'},
            {'dni': '60084632', 'nombres': 'JANAMPA GALVAN YURI', 'licencia': 'P-60084632'},
            {'dni': '43673249', 'nombres': 'QUISPE QUISPE EDILSON', 'licencia': 'H-43673249'},
            {'dni': '45494313', 'nombres': 'PARI CONTRERAS JAIME', 'licencia': 'P-45494313'},
            {'dni': '48125028', 'nombres': 'HUAMAN HANCCO HENRY', 'licencia': 'H-48125028'},
            {'dni': '24805568', 'nombres': 'GOMEZ RIOS ESTANISLAO', 'licencia': 'H-24805568'},
            {'dni': '43750609', 'nombres': 'HUMIRE CARDENAS MANUEL', 'licencia': 'H-43750609'},
            {'dni': '30950158', 'nombres': 'QUISPE HUANACCHIRI, ANDRES', 'licencia': 'F-30950158'},
            {'dni': '46296647', 'nombres': 'HUANCCO CARI ECLER', 'licencia': 'H-46296647'},
            {'dni': '16154820', 'nombres': 'MANGO PALOMINO GREGORIO JOB', 'licencia': 'Q-16154820'},
            {'dni': '44447879', 'nombres': 'SONCO MURILLO EDILBERTO', 'licencia': 'H-44447879'},
            {'dni': '29511147', 'nombres': 'MACHACA ZAPANA MARCELINO HONORIO', 'licencia': 'P-29511147'},
            {'dni': '44607471', 'nombres': 'RESALVE QUISPE MIGUEL', 'licencia': 'R-44607471'},
            {'dni': '30505651', 'nombres': 'DE LA CRUZ NARAZAS DEMETRIO LEANDRO', 'licencia': 'H-30505651'},
            {'dni': '30850664', 'nombres': 'VILLASANTE SONCCO NESTOR', 'licencia': 'H-30850664'},
            {'dni': '44527464', 'nombres': 'MAMANI HUANCCO, MIGUEL', 'licencia': 'U-44527464'},
            {'dni': '30505661', 'nombres': 'DE LA CRUZ NARAZAS DEMETRIO LEANDRO', 'licencia': 'H-30505661'},
            {'dni': '44755156', 'nombres': 'AJAHUANA PACSI RICARDO', 'licencia': 'H-44755156'},
            {'dni': '71626653', 'nombres': 'MEDINA ANGULO JULBER WILSON', 'licencia': 'H-71626653'},
            {'dni': '46874214', 'nombres': 'MELCHOR ROJAS JOSE LUIS', 'licencia': 'H-46874214'},
            {'dni': '30846766', 'nombres': 'MAMANI TIPO JUNA PABLO', 'licencia': 'H-30846766'},
            {'dni': '41955810', 'nombres': 'GELDRES FLORES AGUSTIN ANDRES', 'licencia': 'H-41955810'},
            {'dni': '47549227', 'nombres': 'TICLLAHUANACO SULLCAHUAMAN ROMULO', 'licencia': 'H-47549227'},
            {'dni': '40291910', 'nombres': 'GOMEZ RIOS FLORENTINO', 'licencia': 'H-40291910'},
            {'dni': '46949375', 'nombres': 'HUALLCCA MISAICO JORGE LUIS', 'licencia': 'F-46949375'},
            {'dni': '45329948', 'nombres': 'HUAMAN HANCCO ROLANDO', 'licencia': 'H-45329948'},
            {'dni': '45284135', 'nombres': 'QUISPE CHOQUECCOTA VIDAL ALFREDO', 'licencia': 'H-45284135'},
            {'dni': '46244251', 'nombres': 'LIMA YUPA ALBERTO', 'licencia': 'Z-46244251'},
            {'dni': '46244251', 'nombres': 'LIMA YUPA ALBERTO', 'licencia': 'Z-46244251'},
        ]

        # Limpiar tabla existente
        self.stdout.write("Limpiando tabla de conductores existente...")
        Conductor.objects.all().delete()

        created_count = 0
        skipped_count = 0

        self.stdout.write(f"Importando {len(conductores_data)} conductores...")

        # Fechas por defecto para licencias
        fecha_emision = date(2020, 1, 1)
        fecha_vencimiento = date(2030, 12, 31)

        for i, data in enumerate(conductores_data, 1):
            try:
                # Crear conductor
                conductor = Conductor.objects.create(
                    dni=data['dni'],
                    nombres=data['nombres'],
                    licencia_conducir=data['licencia'],
                    categoria_licencia='A-IIB',  # Categoría por defecto
                    fecha_emision_licencia=fecha_emision,
                    fecha_vencimiento_licencia=fecha_vencimiento,
                    estado=True
                )
                
                created_count += 1
                if i % 10 == 0:  # Mostrar progreso cada 10 registros
                    self.stdout.write(f"Procesados: {i}/{len(conductores_data)}")
                    
            except Exception as e:
                skipped_count += 1
                self.stdout.write(
                    self.style.ERROR(f"✗ Error con {data['dni']}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen del proceso:\n'
                f'   ✓ Conductores creados: {created_count}\n'
                f'   ✗ Omitidos: {skipped_count}\n'
                f'   📋 Total conductores en BD: {Conductor.objects.count()}'
            )
        ) 