from django.shortcuts import render, redirect
from django.views.generic import ListView
from AplicacionPracticas1.models import Practica, FasePractica, EmpresaPractica, Empresa, Usuario, Fase
from AplicacionPracticas1.forms import *
from django.http import Http404
from datetime import datetime, timedelta
from django.db.models import OuterRef, Subquery

from django.forms import formset_factory

from django.template.loader import render_to_string

from django.http import JsonResponse
from django.http import HttpResponseBadRequest

from django.shortcuts import get_object_or_404

def index(request):

    estudiantePractica = Practica.objects.select_related('rut_persona__usuario').all()

    return render(request, 'index.html', {'estudiantePractica': estudiantePractica})

def practica(request):
    practica = Practica.objects.all()
    return render(request, 'practica.html', {'practica': practica})

class listaEstudiantePractica(ListView):
    template_name = "index.html"
    context_object_name = "estudiantePractica"

    def get_queryset(self):

        practicaPorCarrera = Practica.objects.select_related('rut_persona__usuario').all()

        return practicaPorCarrera

    def post(self, request, *args, **kwargs):

        form_fase = FaseForm(request.POST)
        form_carrera = CarreraForm(request.POST)

        for practica_instancia in Practica.objects.all():
            print("hola")
            practica_instancia.fase_ultima()
            fase_practica_instancia = FasePractica.objects.filter(id_practica=practica_instancia).last()
            fase_practica_instancia.cambio_estado(fase_practica_instancia)
            fase_practica_instancia.actualizar_contador()


        estudiantePractica = Practica.objects.select_related('rut_persona__usuario').all()
        filtrado = estudiantePractica

        if form_fase.is_valid():

            fase_seleccionada = form_fase.cleaned_data['fase']

            if fase_seleccionada == '1' or fase_seleccionada == '2' or fase_seleccionada == '3' or fase_seleccionada == '4':

                filtrado = filtrado.filter(fase_actual=fase_seleccionada)
                print(filtrado)

        if form_carrera.is_valid():

            carrera_seleccionada = form_carrera.cleaned_data['carrera']
            filtro_carrera = Usuario.objects.filter(carrera=carrera_seleccionada)

            if carrera_seleccionada == '1' or carrera_seleccionada == '2':

                filtrado = filtrado.filter(rut_persona__in=filtro_carrera)


        return render(request, self.template_name, {'form_fase': form_fase,'form_carrera': form_carrera,
                                                        'estudiantePractica': filtrado})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_fase'] = FaseForm()
        context['form_carrera'] = CarreraForm()
        return context

class listaPractica(ListView):
    template_name = "practica.html"
    context_object_name = "practica"

    def get_queryset(self):
        # Identificar Practica
        practica_id = self.kwargs["pk"]
        listaP = Practica.objects.filter(id_practica=practica_id)

        return listaP

    def post(self, request, *args, **kwargs):
        practica_id = self.kwargs['pk']
        practica_instance = Practica.objects.get(id_practica=practica_id)

        try:
            fase_practica_instance = FasePractica.objects.filter(id_practica=practica_id).last()

            archivos_instances = Archivo.objects.filter(fase_practica=fase_practica_instance).all()


            num_fase = FasePractica.objects.filter(id_practica=practica_id).count() + 1

            if num_fase == 5:
                num_fase = 4

            fase_siguiente_instance = Fase.objects.get(fase=num_fase)

            #fases = ["Inscripción", "Realización", "Término", "Evaluación"]
            #siguiente_fase = fases[num_fase]

        except FasePractica.DoesNotExist:
            raise Http404("La FasePractica no existe para la Practica especificada")

        try:
            estudiante_instance = Usuario.objects.get(rut_persona=practica_instance.rut_persona.rut_persona)

        except FasePractica.DoesNotExist:
            raise Http404("La Estudiante no existe para la Practica especificada")

        form_practica = PracticaForm(request.POST, instance=practica_instance,
                                          initial={'id_practica': fase_practica_instance.id_practica,
                                                    'fase': fase_practica_instance.fase})

        form_fasePractica = FasePracticaForm(request.POST,
                                          initial={'id_practica': practica_instance.id_practica,
                                                    'fase': fase_siguiente_instance.fase,
                                                   'conteo': 30})

        form_estudiante = EstudianteForm(request.POST, instance=estudiante_instance,
                                           initial={'rut_persona': estudiante_instance.rut_persona,
                                                    'contrasena': estudiante_instance.contrasena,
                                                    'carrera': estudiante_instance.carrera})

        form_empresa = EmpresaForm(request.POST)
        form_supervisor = EmpresaPracticaForm(request.POST)

        if form_practica.is_valid():
            form_practica.save()
            return redirect('listaPractica', pk=practica_id)


        if form_empresa.is_valid() and form_supervisor.is_valid():

            empresa_instance = form_empresa.save()
            print("empresa_instance.rut_empresa:", empresa_instance.rut_empresa)

            form_supervisor.instance.rut_empresa = empresa_instance
            form_supervisor.instance.id_practica = practica_instance
            print("form_supervisor.instance.rut_empresa:", form_supervisor.instance.rut_empresa)

            if form_supervisor.is_valid():
                form_supervisor.save()
                print("Guardado exitosamente")
                return redirect('listaPractica', pk=practica_id)
            else:
                print("form_supervisor.errors:", form_supervisor.errors)

        if form_estudiante.is_valid():
            form_estudiante.save()
            return redirect('listaPractica', pk=practica_id)


        lista_archivos = []

        for a in archivos_instances:
            form_archivo = ArchivoForm(request.POST, request.FILES, prefix=f'form_{a.documento}', instance=a,
                                       initial={'fase_practica': fase_practica_instance, 'documento': a.documento})
            lista_archivos.append({
            'formulario': form_archivo,
            'nombre': a.documento,  # Puedes ajustar esto según tu necesidad
            })

            if form_archivo.is_valid():
                form_archivo.save()
                fase_practica_instance.contar_guardados(archivos_instances)

        if fase_practica_instance.conteo <= 0:

            if form_fasePractica.is_valid():

                form_fasePractica.save(commit=False)
                form_fasePractica.instance.id_practica = practica_instance
                form_fasePractica.instance.fase = fase_siguiente_instance

                # Inicialización de Conteo (días) según la Fecha que corresponde por Fase

                if fase_siguiente_instance.fase == 1:

                    diferencia = practica_instance.fechaInicio - practica_instance.fechaCreación
                    dias_diferencia = diferencia.days
                    form_fasePractica.instance.conteo = dias_diferencia

                elif fase_siguiente_instance.fase == 2:

                    diferencia = practica_instance.fechaFin - practica_instance.fechaInicio
                    dias_diferencia = diferencia.days
                    form_fasePractica.instance.conteo = dias_diferencia

                elif fase_siguiente_instance.fase == 2:

                    diferencia = practica_instance.fechaFin - practica_instance.fechaInicio
                    dias_diferencia = diferencia.days
                    form_fasePractica.instance.conteo = dias_diferencia

                elif fase_siguiente_instance.fase == 3:

                    dias_diferencia = 15
                    form_fasePractica.instance.conteo = dias_diferencia

                elif fase_siguiente_instance.fase == 4:

                    fase_siguiente_instance = 30 - fase_practica_instance.conteo


                form_fasePractica.save()

                for doc in Documento.objects.filter(fase=fase_siguiente_instance):
                    Archivo.objects.create(fase_practica=form_fasePractica.instance, documento=doc.documento)


            return redirect('listaPractica', pk=practica_id)


        return render(request, self.template_name, {'form_practica': form_practica, 'form_fasePractica': form_fasePractica, 'form_archivo': form_archivo, 'lista_archivos':lista_archivos, 'form_empresa': form_empresa,
                                                    'form_supervisor': form_supervisor, 'form_estudiante': form_estudiante,
                                                    'practica': self.get_queryset()})


    def get_context_data(self, **kwargs):

        lista_archivos = []

        context = super().get_context_data(**kwargs)
        context['form_practica'] = PracticaForm()
        context['form_fasePractica'] = FasePracticaForm()
        context['form_archivo'] = ArchivoForm()
        context['form_empresa'] = EmpresaForm()
        context['form_supervisor'] = EmpresaPracticaForm()
        context['form_estudiante'] = EstudianteForm()

        return context