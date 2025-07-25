# Generated by Django 5.2.1 on 2025-05-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0006_alter_ley_lote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ley',
            name='ley_onz_tc',
            field=models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Ley (onz/tc)'),
        ),
        migrations.AlterField(
            model_name='ley',
            name='tms',
            field=models.DecimalField(decimal_places=3, max_digits=10, verbose_name='TMS'),
        ),
    ]
