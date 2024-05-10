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
        fields = ['fechaInicio', 'fechaFin', 'modalidad']

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

class RubroForm(forms.Form):
        rubros = (("0", "Rubro"),
              ("1", "Agropecuaria-Silvícola"),
              ("2", "Construcción"),
              ("3", "Pesca"),
              ("4", "Trasportes y Comunicaciones"),
              ("5", "Industria Manufactura"),
              ("6", "Electricidad, Gas y Agua"),
              ("7", "Administración Pública"),
              ("8", "Comercio, restaurantes y hoteles"),
              ("9", "Servicios Personales"),
              ("10", "Minería"),
              ("11", "Servicios Financieros y Empresariales"),
              ("12", "Propiedad de Vivienda"),
              ("13", "Otros"))
        rubro = forms.ChoiceField(choices=rubros, required=False, label="", initial=['0'], )


class ModalidadForm(forms.Form):
    modalidades = (("0", "Modalidad"),("1", "Presencial"), ("2", "Híbrido"), ("3", "Remoto"))
    modalidad = forms.ChoiceField(choices=modalidades, required=False, label="", initial=['0'], )

class SectorForm(forms.Form):
    sectores = (("0", "Sector"),("1", "Pública"), ("2", "Privada"))
    sector = forms.ChoiceField(choices=sectores, required=False, label="", initial=['0'], )
class TamanoForm(forms.Form):
    tamanos = (("0", "Tamaño"),("1", "Micro"),("2", "Pequeña"), ("3", "Mediana"), ("4", "Grande"))
    tamano = forms.ChoiceField(choices=tamanos, required=False, label="", initial=['0'], )

#class BuscadorFOrm(forms.Form):

        #buscador = forms.CharField(max_length=20, null=True)