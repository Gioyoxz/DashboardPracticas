from django import forms
from .models import *
from multiupload.fields import MultiFileField

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_persona', 'carrera', 'correo_persona', 'telefono_persona']

class PracticaForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = ['fechaInicio', 'fechaFin', 'horas']

class FasePracticaForm(forms.ModelForm):
    class Meta:
        model = FasePractica
        fields = []

class ArchivoForm(forms.ModelForm):

    class Meta:
        model = Archivo
        fields = ['archivo']

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['rut_empresa', 'nombre_empresa', 'rubro_empresa']

class EmpresaPracticaForm(forms.ModelForm):
    class Meta:
        model = EmpresaPractica
        fields = ['nombre_supervisor', 'correo_supervisor', 'telefono_supervisor']

class AprobadoForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = []

class Reprobado(forms.ModelForm):
    class Meta:
        model = Practica
        fields = []

class CarreraForm(forms.Form):

        carreras = (("0", "Carrera"), ("1", "IC"), ("2", "IICG"))
        carrera = forms.ChoiceField(choices=carreras, required=False, label="", initial=['0'],)

class FaseForm(forms.Form):

        fases = (("0", "Fase"), ("1", "Inscripción"), ("2", "Inicio"), ("3", "Término"), ("4", "Informe"), ("5", "Evaluación"))
        fase = forms.ChoiceField(choices=fases, required=False, label="", initial=['0'], )

class EstadoForm(forms.Form):
        estados = (("0", "Estado"), ("1", "Vencido"), ("2", "Pendiente"), ("3", "Completado"))
        estado = forms.ChoiceField(choices=estados, required=False, label="", initial=['0'], )

class BuscadorForm(forms.Form):

        buscar = forms.CharField(required=False, label="")

class CrearPracticaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut_persona']

#class BuscadorFOrm(forms.Form):

        #buscador = forms.CharField(max_length=20, null=True)