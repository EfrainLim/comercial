# Generated by Django 5.2.1 on 2025-07-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balanza', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanza',
            name='cantidad_sacos',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad de Sacos'),
        ),
        migrations.AddField(
            model_name='balanza',
            name='tipo_empaque',
            field=models.CharField(blank=True, choices=[('GRANEL', 'A GRANEL'), ('SACOS', 'SACOS')], max_length=10, null=True, verbose_name='Tipo de Empaque'),
        ),
    ]
