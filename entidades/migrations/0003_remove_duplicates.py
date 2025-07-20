from django.db import migrations

def remove_duplicates(apps, schema_editor):
    ProveedorIngemmet = apps.get_model('entidades', 'ProveedorIngemmet')
    # Obtener todos los códigos duplicados
    from django.db.models import Count
    duplicates = ProveedorIngemmet.objects.values('codigo_ingemmet').annotate(
        count=Count('codigo_ingemmet')).filter(count__gt=1)
    
    # Para cada código duplicado, mantener solo el registro más reciente
    for dup in duplicates:
        codigo = dup['codigo_ingemmet']
        records = ProveedorIngemmet.objects.filter(codigo_ingemmet=codigo).order_by('-id')
        # Mantener el primer registro (más reciente) y eliminar los demás
        for record in records[1:]:
            record.delete()

class Migration(migrations.Migration):
    dependencies = [
        ('entidades', '0002_alter_proveedoringemmet_unique_together_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates),
    ] 