from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('entidades', '0003_remove_duplicates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedoringemmet',
            name='codigo_ingemmet',
            field=models.CharField(max_length=50, unique=True, verbose_name='Código INGEMMET'),
        ),
    ] 