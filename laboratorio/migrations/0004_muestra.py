# Generated by Django 5.2.1 on 2025-05-13 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0003_initial'),
        ('lotes', '0004_alter_lote_codigo_sistema_alter_lote_nro_sacos'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Muestra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_muestra', models.CharField(max_length=20, unique=True, verbose_name='Código Muestra')),
                ('fecha_recepcion', models.DateField(verbose_name='Fecha Recepción')),
                ('tipo_analisis', models.CharField(choices=[('au_ag', 'Au-Ag'), ('cu', 'Cu'), ('pb_zn', 'Pb-Zn')], max_length=10, verbose_name='Tipo Análisis')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En Proceso'), ('completado', 'Completado')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('fecha_resultado', models.DateField(blank=True, null=True, verbose_name='Fecha Resultado')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lotes.lote', verbose_name='Lote')),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='muestras_creadas', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='muestras_modificadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Muestra',
                'verbose_name_plural': 'Muestras',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
