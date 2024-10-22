# Generated by Django 4.2.7 on 2024-05-02 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AplicacionPracticas1', '0011_alter_empresa_rubro_empresa_alter_practica_condicion'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='sector',
            field=models.CharField(choices=[('1', 'Pública'), ('2', 'Privada')], default='1', verbose_name='Sector'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='tamano',
            field=models.CharField(choices=[('1', 'Micro'), ('2', 'Pequeña'), ('3', 'Mediana'), ('4', 'Grande')], default='1', verbose_name='Tamaño'),
        ),
        migrations.AddField(
            model_name='practica',
            name='modalidad',
            field=models.CharField(choices=[('1', 'Presencial'), ('2', 'Híbrido'), ('3', 'Remoto')], default='1', verbose_name='Condicion'),
        ),
    ]
