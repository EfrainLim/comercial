# Generated by Django 5.2.1 on 2025-05-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0009_tipoproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoproducto',
            name='es_mineral',
            field=models.BooleanField(default=False, verbose_name='Es Mineral'),
        ),
    ]
