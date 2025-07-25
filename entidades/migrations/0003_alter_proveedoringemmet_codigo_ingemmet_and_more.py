# Generated by Django 5.2.1 on 2025-05-12 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0002_alter_proveedoringemmet_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedoringemmet',
            name='codigo_ingemmet',
            field=models.CharField(max_length=50, unique=True, verbose_name='Código INGEMMET'),
        ),
        migrations.AlterField(
            model_name='proveedoringemmet',
            name='estado',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='proveedoringemmet',
            name='procedencia',
            field=models.CharField(max_length=100, verbose_name='Procedencia'),
        ),
    ]
