# Generated by Django 4.2.7 on 2024-05-02 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AplicacionPracticas1', '0012_empresa_sector_empresa_tamano_practica_modalidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practica',
            name='condicion',
            field=models.CharField(choices=[('1', 'Cursando'), ('2', 'Cancelado'), ('3', 'Aprobado'), ('4', 'Rechazado')], default='1', verbose_name='Condición'),
        ),
        migrations.AlterField(
            model_name='practica',
            name='modalidad',
            field=models.CharField(choices=[('1', 'Presencial'), ('2', 'Híbrido'), ('3', 'Remoto')], default='1', verbose_name='Modalidad'),
        ),
    ]
