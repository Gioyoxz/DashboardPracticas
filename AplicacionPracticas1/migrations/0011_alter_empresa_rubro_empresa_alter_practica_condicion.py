# Generated by Django 4.2.7 on 2024-05-02 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AplicacionPracticas1', '0010_alter_practica_condicion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='rubro_empresa',
            field=models.CharField(choices=[('1', 'Agropecuaria-Silvícola'), ('2', 'Construcción'), ('3', 'Pesca'), ('4', 'Trasportes y Comunicaciones'), ('5', 'Industria Manufactura'), ('6', 'Electricidad, Gas y Agua'), ('7', 'Administración Pública'), ('8', 'Comercio, restaurantes y hoteles'), ('9', 'Servicios Personales'), ('10', 'Minería'), ('11', 'Servicios Financieros y Empresariales'), ('12', 'Propiedad de Vivienda'), ('13', 'Otros')], default='10', max_length=50, verbose_name='Rubro'),
        ),
        migrations.AlterField(
            model_name='practica',
            name='condicion',
            field=models.CharField(choices=[('1', 'Cursando'), ('2', 'Cancelado'), ('3', 'Aprobado'), ('4', 'Rechazado')], default='1', verbose_name='Condicion'),
        ),
    ]