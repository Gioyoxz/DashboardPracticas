# Generated by Django 4.2.7 on 2023-12-24 22:45

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrera', models.CharField(blank=True, choices=[('1', 'Ingeniería Comercial'), ('2', 'Ingeniería en Información y Control de gestión')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('rut_empresa', models.CharField(help_text='(Sin puntos ni guión)', max_length=12, primary_key=True, serialize=False, verbose_name='Rut')),
                ('nombre_empresa', models.CharField(max_length=50, verbose_name='Nombre')),
                ('rubro_empresa', models.CharField(max_length=50, verbose_name='Rubro')),
            ],
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fase', models.CharField(blank=True, choices=[('1', 'Inscripción'), ('2', 'Inicio'), ('3', 'Término'), ('4', 'Informe')], max_length=50, verbose_name='Fase de')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('rut_persona', models.CharField(help_text='Ingrese Rut o Dni sin puntos ni guión', max_length=12, primary_key=True, serialize=False, verbose_name='Rut o Dni')),
                ('nombre_persona', models.CharField(max_length=50, verbose_name='Nombre')),
                ('correo_persona', models.CharField(max_length=40, verbose_name='Correo')),
                ('telefono_persona', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='+569XXXXXX', max_length=128, region=None, verbose_name='Telefono')),
            ],
        ),
        migrations.CreateModel(
            name='Practica',
            fields=[
                ('id_practica', models.AutoField(primary_key=True, serialize=False)),
                ('fechaCreación', models.DateField(max_length=50, null=True, verbose_name='Fecha de Creación')),
                ('fechaInicio', models.DateField(max_length=50, null=True, verbose_name='Fecha de Inicio')),
                ('fechaFin', models.DateField(max_length=30, null=True, verbose_name='Fecha de Fin')),
                ('horas', models.IntegerField(null=True, verbose_name='Horas')),
                ('observacion', models.CharField(max_length=50, null=True, verbose_name='Observación')),
                ('fase_actual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.fase')),
                ('rut_persona', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.persona')),
            ],
        ),
        migrations.CreateModel(
            name='FasePractica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_conteo', models.DateField(auto_now_add=True, max_length=50, verbose_name='Fecha fin')),
                ('conteo', models.IntegerField(null=True, verbose_name='Conteo')),
                ('estado', models.CharField(choices=[('1', 'Pendiente'), ('2', 'Completado'), ('3', 'Vencido')], default=1, verbose_name='Estado')),
                ('fase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.fase')),
                ('id_practica', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.practica')),
            ],
            options={
                'unique_together': {('id_practica', 'fase')},
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.CharField(blank=True, choices=[('1', 'Formulario de Inscripción'), ('2', 'Plan de Trabajo'), ('3', 'Carta de Aceptación'), ('4', 'Carta de Compromiso'), ('5', 'Constancia de Termino'), ('6', 'Informe de Práctica')], max_length=50, verbose_name='Documento')),
                ('fase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.fase')),
            ],
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(null=True, upload_to='attachments')),
                ('documento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AplicacionPracticas1.documento')),
                ('fase_practica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AplicacionPracticas1.fasepractica')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AplicacionPracticas1.persona')),
                ('contrasena', models.CharField(max_length=50, verbose_name='Contraseña')),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.carrera')),
            ],
            bases=('AplicacionPracticas1.persona',),
        ),
        migrations.CreateModel(
            name='EmpresaPractica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_empresa_practica', models.DateField(auto_now_add=True, max_length=50, verbose_name='Fecha')),
                ('nombre_supervisor', models.CharField(max_length=30, null=True, verbose_name='Supervisor')),
                ('correo_supervisor', models.CharField(max_length=30, null=True, verbose_name='Correo')),
                ('telefono_supervisor', phonenumber_field.modelfields.PhoneNumberField(help_text='(+569XXXXXX)', max_length=128, null=True, region=None, verbose_name='Telefono')),
                ('id_practica', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.practica')),
                ('rut_empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AplicacionPracticas1.empresa')),
            ],
            options={
                'unique_together': {('rut_empresa', 'id_practica')},
            },
        ),
    ]
