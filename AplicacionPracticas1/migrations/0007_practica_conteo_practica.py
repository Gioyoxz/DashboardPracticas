# Generated by Django 4.2.7 on 2024-03-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AplicacionPracticas1', '0006_practica_estado_practica_alter_carrera_carrera_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='practica',
            name='conteo_practica',
            field=models.IntegerField(null=True, verbose_name='Conteo'),
        ),
    ]
