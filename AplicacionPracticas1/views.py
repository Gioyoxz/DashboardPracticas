from django.shortcuts import render, redirect
from django.views.generic import ListView
from AplicacionPracticas1.models import Practica, FasePractica, EmpresaPractica, Empresa, Usuario, Fase
from AplicacionPracticas1.forms import *
from django.http import Http404
from datetime import datetime, timedelta
from django.db.models import OuterRef, Subquery
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.utils import timezone
from datetime import timedelta

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
        practicaPorCarrera = practicaPorCarrera.order_by('estado_practica', 'conteo_practica')

        return practicaPorCarrera

    def post(self, request, *args, **kwargs):

        hoy = timezone.now().date()
        plazo_14 = hoy + timedelta(days=14)

        form_fase = FaseForm(request.POST)
        form_carrera = CarreraForm(request.POST)
        form_estado = EstadoForm(request.POST)
        form_buscador = BuscadorForm(request.POST)
        form_crear = CrearPracticaForm(request.POST)

        estudiantePractica = Practica.objects.select_related('rut_persona__usuario').all()
        estudiantePractica = estudiantePractica.order_by('estado_practica', 'conteo_practica')

        filtrado = estudiantePractica

        barra_vencido = 0
        barra_pendiente = 0
        barra_completado = 0


        if form_crear.is_valid():

            form_crear.save(commit=False)

            try:
                estudiante_instance = Usuario.objects.get(rut_persona=form_crear.instance.rut_persona)

            except ObjectDoesNotExist:
                estudiante_instance = None

            if estudiante_instance == None:
                estudiante_instance = Usuario.objects.create(rut_persona=form_crear.instance.rut_persona)

            practica_instance = Practica.objects.create(rut_persona=estudiante_instance)
            fase_instance = Fase.objects.get(fase='1')
            fase_practica_instance = FasePractica.objects.create(id_practica=practica_instance, fase=fase_instance, conteo=14, fecha_conteo=plazo_14)

            for doc in Documento.objects.filter(fase=fase_instance):
                Archivo.objects.create(fase_practica=fase_practica_instance, documento=doc)

            return redirect('listaPractica', pk=practica_instance.id_practica)

        if form_fase.is_valid():

            fase_seleccionada = form_fase.cleaned_data['fase']

            if fase_seleccionada == '1' or fase_seleccionada == '2' or fase_seleccionada == '3' or fase_seleccionada == '4' or fase_seleccionada == '5':

                filtrado = filtrado.filter(fase_actual=fase_seleccionada)

        if form_carrera.is_valid():

            carrera_seleccionada = form_carrera.cleaned_data['carrera']
            filtro_carrera = Usuario.objects.filter(carrera=carrera_seleccionada)

            if carrera_seleccionada == '1' or carrera_seleccionada == '2':

                filtrado = filtrado.filter(rut_persona__in=filtro_carrera)

        if form_estado.is_valid():

            estado_seleccionado = form_estado.cleaned_data['estado']

            if estado_seleccionado == '1' or estado_seleccionado == '2' or estado_seleccionado == '3':

                filtrado = filtrado.filter(estado_practica=estado_seleccionado)

        if form_buscador.is_valid():

            texto_buscar = form_buscador.cleaned_data['buscar']

            if texto_buscar != "" and not texto_buscar.isdigit():

                filtrado = filtrado.filter(rut_persona__nombre_persona__icontains=texto_buscar)

            elif texto_buscar.isdigit():

                filtrado = filtrado.filter(rut_persona__rut_persona__icontains=texto_buscar)


        for practica_instancia in filtrado:
            practica_instancia.fase_ultima()
            practica_instancia.estado_actual()
            practica_instancia.conteo_actual()
            fase_practica_instancia = FasePractica.objects.filter(id_practica=practica_instancia).last()
            fase_practica_instancia.actualizar_contador()
            fase_practica_instancia.cambio_estado(fase_practica_instancia)

            if fase_practica_instancia.estado == 1 or fase_practica_instancia.estado == "1":
                barra_vencido += 1

            elif fase_practica_instancia.estado == 2 or fase_practica_instancia.estado == "2":
                barra_pendiente += 1

            elif fase_practica_instancia.estado == 3 or fase_practica_instancia.estado == "3":
                barra_completado += 1

        filtro_ic = Usuario.objects.filter(carrera='1')
        filtro_iicg = Usuario.objects.filter(carrera='2')

        barra_ic = filtrado.filter(rut_persona__in=filtro_ic).count()
        barra_iicg = filtrado.filter(rut_persona__in=filtro_iicg).count()

        barra_fase1 = filtrado.filter(fase_actual="1").count()
        barra_fase2 = filtrado.filter(fase_actual="2").count()
        barra_fase3 = filtrado.filter(fase_actual="3").count()
        barra_fase4 = filtrado.filter(fase_actual="4").count()
        barra_fase5 = filtrado.filter(fase_actual="5").count()


        return render(request, self.template_name, {'form_buscador':form_buscador,'form_fase': form_fase,'form_carrera': form_carrera, 'form_estado': form_estado, 'form_crear': form_crear,
                                                        'estudiantePractica': filtrado, 'barra_ic': barra_ic, 'barra_iicg': barra_iicg, 'barra_fase1':barra_fase1, 'barra_fase2':barra_fase2,
                                                    'barra_fase3':barra_fase3, 'barra_fase4':barra_fase4, 'barra_fase5':barra_fase5, 'barra_vencido':barra_vencido, 'barra_pendiente':barra_pendiente,
                                                    'barra_completado':barra_completado})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        practicaPorCarrera = self.get_queryset()
        practicaPorCarrera = practicaPorCarrera.order_by('estado_practica', 'conteo_practica')

        barra_vencido = 0
        barra_pendiente = 0
        barra_completado = 0

        for practica_instancia in Practica.objects.all():
            practica_instancia.fase_ultima()
            practica_instancia.estado_actual()
            practica_instancia.conteo_actual()
            fase_practica_instancia = FasePractica.objects.filter(id_practica=practica_instancia).last()
            fase_practica_instancia.actualizar_contador()
            fase_practica_instancia.cambio_estado(fase_practica_instancia)

            if fase_practica_instancia.estado == 1 or fase_practica_instancia.estado == "1":
                barra_vencido += 1

            elif fase_practica_instancia.estado == 2 or fase_practica_instancia.estado == "2":
                barra_pendiente += 1

            elif fase_practica_instancia.estado == 3 or fase_practica_instancia.estado == "3":
                barra_completado += 1


        barra_ic = Usuario.objects.filter(carrera='1').count()
        barra_iicg = Usuario.objects.filter(carrera='2').count()

        barra_fase1 = practicaPorCarrera.filter(fase_actual="1").count()
        barra_fase2 = practicaPorCarrera.filter(fase_actual="2").count()
        barra_fase3 = practicaPorCarrera.filter(fase_actual="3").count()
        barra_fase4 = practicaPorCarrera.filter(fase_actual="4").count()
        barra_fase5 = practicaPorCarrera.filter(fase_actual="5").count()

        context['barra_ic'] = barra_ic
        context['barra_iicg'] = barra_iicg
        context['barra_fase1'] = barra_fase1
        context['barra_fase2'] = barra_fase2
        context['barra_fase3'] = barra_fase3
        context['barra_fase4'] = barra_fase4
        context['barra_fase5'] = barra_fase5

        context['barra_vencido'] = barra_vencido
        context['barra_pendiente'] = barra_pendiente
        context['barra_completado'] = barra_completado

        context['form_fase'] = FaseForm()
        context['form_carrera'] = CarreraForm()
        context['form_estado'] = EstadoForm()
        context['form_buscador'] = BuscadorForm()
        context['form_crear'] = CrearPracticaForm

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
        estudiante_instance = Usuario.objects.get(rut_persona=practica_instance.rut_persona.rut_persona)

        fase_practica_instance = FasePractica.objects.filter(id_practica=practica_id).last()
        cantidad_fase = FasePractica.objects.filter(id_practica=practica_id).count()
        fase_practica_instance.actualizar_contador()
        archivos_instances = Archivo.objects.filter(fase_practica=fase_practica_instance).all().order_by("documento")
        sup = None
        fase_practica_instance.cambio_estado(fase_practica_instance)
        practica_instance.actualizar_estado()

        try:
            supervisor_instance = EmpresaPractica.objects.get(id_practica=practica_instance)
            print("try1")
        except ObjectDoesNotExist:
            print("except1")
            supervisor_instance = None

        try:
            print("try2")
            if supervisor_instance != None:
                print("if supervisor_instance != None:")
                empresa_instance = Empresa.objects.get(rut_empresa=supervisor_instance.rut_empresa.rut_empresa)
            else:
                print("elsetry")
                empresa_instance = None
        except ObjectDoesNotExist:
            empresa_instance = None
            print("except2")

        num_fase = FasePractica.objects.filter(id_practica=practica_id).count() + 1

        if num_fase == 5:
            num_fase = 4

        fase_siguiente_instance = Fase.objects.get(fase=num_fase)

            #fases = ["Inscripción", "Realización", "Término", "Evaluación"]
            #siguiente_fase = fases[num_fase]


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

        form_empresa = EmpresaForm(request.POST, instance=empresa_instance)

        if supervisor_instance == None:
            print("if supervisor_instance == None:")
            form_supervisor = EmpresaPracticaForm(request.POST)

        else:
            print("else:")
            form_supervisor = EmpresaPracticaForm(request.POST, instance=supervisor_instance,)

        if form_practica.is_valid():
            form_practica.save()
            fase_practica_instance.actualizar_contador()
            fase_practica_instance.cambio_estado(fase_practica_instance)
            return redirect('listaPractica', pk=practica_id)

        print(form_empresa.errors)

        if form_empresa.is_valid() and form_supervisor.is_valid():

            print("is valid")

            empresa_instance = form_empresa.save()

            if form_supervisor:

                form_supervisor.instance.rut_empresa = empresa_instance
                form_supervisor.instance.id_practica = practica_instance

            if form_supervisor.is_valid():
                form_supervisor.save()
                fase_practica_instance.cambio_estado(fase_practica_instance)
                return redirect('listaPractica', pk=practica_id)
            else:
                print("form_supervisor.errors:", form_supervisor.errors)

        if not form_empresa.is_valid() and form_supervisor.is_valid():

            try:
                empresa_instance = Empresa.objects.get(rut_empresa=form_empresa.instance.rut_empresa)

            except:
                empresa_instance = None

            if empresa_instance != None:

                if form_supervisor:
                    form_supervisor.instance.rut_empresa = empresa_instance
                    form_supervisor.instance.id_practica = practica_instance

                if form_supervisor.is_valid():
                    form_supervisor.save()
                    fase_practica_instance.cambio_estado(fase_practica_instance)
                    return redirect('listaPractica', pk=practica_id)
                else:
                    print("form_supervisor.errors:", form_supervisor.errors)

        if form_estudiante.is_valid():
            form_estudiante.save()
            fase_practica_instance.cambio_estado(fase_practica_instance)
            return redirect('listaPractica', pk=practica_id)


        form_archivo = modelformset_factory(Archivo,form=ArchivoForm, extra=0)
        formset = form_archivo(request.POST, request.FILES, queryset=archivos_instances)
        recarga = False
        vuelta = 0


        for f, a in zip(formset, archivos_instances):
            vuelta += 1

            if f.is_valid():

                recarga = True
                f.save(commit=False)

                if (f.instance.archivo != None) and (f.instance.archivo != ""):

                    a.archivo = f.instance.archivo
                    a.save()
                    fase_practica_instance.contar_guardados(archivos_instances)

            if (recarga == True) and (vuelta == archivos_instances.count()):
                fase_practica_instance.cambio_estado(fase_practica_instance)
                practica_instance.actualizar_estado()

                return redirect('listaPractica', pk=practica_id)

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


        return render(request, self.template_name, {'form_practica': form_practica, 'form_fasePractica': form_fasePractica, 'form_archivo': formset, 'archivos_instances':archivos_instances, 'formset': formset,'form_empresa': form_empresa,
                                                    'form_supervisor': form_supervisor, 'form_estudiante': form_estudiante, 'cantidad_fase': cantidad_fase, 'practica_id': practica_id,
                                                    'practica': self.get_queryset()})

    def get_context_data(self, **kwargs):

        practica_id = self.kwargs['pk']

        practica_instance = Practica.objects.get(id_practica=practica_id)
        fase_practica_instance = FasePractica.objects.filter(id_practica=practica_id).last()
        cantidad_fase = FasePractica.objects.filter(id_practica=practica_id).count()
        archivos_instances = Archivo.objects.filter(fase_practica=fase_practica_instance).all()
        estudiante_instance = Usuario.objects.get(rut_persona=practica_instance.rut_persona.rut_persona)

        form_archivo = modelformset_factory(Archivo, form=ArchivoForm, extra=0)
        formset = form_archivo(queryset=archivos_instances)

        try:
            supervisor_instance = EmpresaPractica.objects.get(id_practica=practica_instance)
        except ObjectDoesNotExist:
            supervisor_instance = None

        try:
            if supervisor_instance != None:
                empresa_instance = Empresa.objects.get(rut_empresa=supervisor_instance.rut_empresa.rut_empresa)
            else:
                empresa_instance = None
        except ObjectDoesNotExist:
            empresa_instance = None


        context = super().get_context_data(**kwargs)
        context['form_practica'] = PracticaForm(instance=practica_instance)
        context['form_fasePractica'] = FasePracticaForm()
        context['form_archivo'] = formset
        context['form_empresa'] = EmpresaForm(instance=empresa_instance)
        context['form_supervisor'] = EmpresaPracticaForm(instance=supervisor_instance)
        context['form_estudiante'] = EstudianteForm(instance=estudiante_instance)
        context['archivos_instances'] = archivos_instances
        context['cantidad_fase'] = cantidad_fase
        context['practica_id'] = practica_id
        context['practica_instance'] = practica_instance

        return context

def cambiar_condicion(request, practica_id, nueva_condicion):
        practica = Practica.objects.get(id_practica=practica_id)
        practica.condicion = nueva_condicion
        practica.save()
        return redirect('listaPractica', pk=practica_id)