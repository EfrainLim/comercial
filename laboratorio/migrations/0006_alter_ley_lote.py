# Generated by Django 5.2.1 on 2025-05-13 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0005_alter_ley_options_remove_ley_fecha_actualizacion_and_more'),
        ('lotes', '0004_alter_lote_codigo_sistema_alter_lote_nro_sacos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ley',
            name='lote',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lotes.lote', verbose_name='Lote'),
        ),
    ]
