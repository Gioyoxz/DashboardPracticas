# Generated by Django 4.2.7 on 2024-03-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AplicacionPracticas1', '0008_alter_fasepractica_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='practica',
            name='condicion',
            field=models.CharField(choices=[('1', 'Cursando'), ('2', 'Cancelado'), ('3', 'Aprobado'), ('4', 'Reprobado')], default='1', verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='fase',
            name='fase',
            field=models.CharField(blank=True, choices=[('1', 'Inscripción'), ('2', 'Inicio'), ('3', 'Término'), ('4', 'Informe'), ('5', 'Evaluación')], max_length=50, verbose_name='Fase de'),
        ),
        migrations.AlterField(
            model_name='fasepractica',
            name='estado',
            field=models.CharField(choices=[('1', 'Vencido'), ('2', 'Pendiente'), ('3', 'Completado')], default='2', verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='fasepractica',
            name='fecha_conteo',
            field=models.DateField(max_length=50, null=True, verbose_name='Fecha conteo'),
        ),
        migrations.AlterField(
            model_name='practica',
            name='estado_practica',
            field=models.CharField(choices=[('1', 'Pendiente'), ('2', 'Completado'), ('3', 'Vencido')], default='2', verbose_name='Estado'),
        ),
    ]