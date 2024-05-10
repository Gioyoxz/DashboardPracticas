from AplicacionPracticas1.views.__init__ import *

def practica(request):
    practica = Practica.objects.all()
    return render(request, 'practica.html', {'practica': practica})

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
        practica_instance.estado_actual()

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
            print('form_estudiante.saveeeeeeeeeeeeeeeeeeeeeeeeeeee()')
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

                    print(Documento.objects.get(documento="1"))

                    if a.documento == Documento.objects.get(documento="1"):

                        print('if a.documento == "1":')

                        doc = Document(a.archivo.path)
                        indice_tabla = 0
                        indice_fila = 0
                        indice_celda = 0
                        name_empresa = ''

                        for table in doc.tables:
                            indice_tabla += 1
                            indice_fila = 0
                            indice_celda = 0

                            for row in table.rows:
                                indice_fila += 1
                                indice_celda = 0

                                for cell in row.cells:
                                    indice_celda += 1

                                    text_without_newlines = cell.text.replace('\n', ' ').strip()
                                    if text_without_newlines:

                                        if indice_tabla == 1:
                                            if indice_celda == 2:

                                                if indice_fila == 2:
                                                    estudiante_instance.nombre_persona = text_without_newlines

                                                elif indice_fila == 4:
                                                    estudiante_instance.telefono_persona = text_without_newlines

                                                elif indice_fila == 5:
                                                    estudiante_instance.correo_persona = text_without_newlines


                                        elif indice_tabla == 3:
                                            if indice_celda == 2:

                                                if indice_fila == 2:
                                                    name_empresa = text_without_newlines

                                                elif indice_fila == 3:

                                                    try:
                                                        empresa_instance = Empresa.objects.get(rut_empresa=text_without_newlines)

                                                    except:
                                                        empresa_instance = Empresa.objects.create(rut_empresa=text_without_newlines)

                                                    try:
                                                        supervisor_instance = EmpresaPractica.objects.get(rut_empresa=empresa_instance, id_practica=practica_instance)
                                                        print("tryyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                                                    except:
                                                        supervisor_instance = EmpresaPractica.objects.create(rut_empresa=empresa_instance, id_practica=practica_instance)
                                                        print("excepttttttttttttttttttttttttt")

                                                    empresa_instance.nombre_empresa = name_empresa

                                                elif indice_fila == 6:
                                                    supervisor_instance.nombre_supervisor = text_without_newlines

                                                elif indice_fila == 5:
                                                    supervisor_instance.telefono_supervisor = text_without_newlines

                                                elif indice_fila == 8:
                                                    supervisor_instance.correo_supervisor = text_without_newlines

                                        elif indice_tabla == 9:
                                            if indice_celda == 2:

                                                if indice_fila == 1:
                                                    practica_instance.fechaInicio = datetime.strptime(text_without_newlines, "%d/%m/%Y").date()

                                                elif indice_fila == 2:
                                                    practica_instance.fechaFin = datetime.strptime(text_without_newlines, "%d/%m/%Y").date()

                        estudiante_instance.save()
                        empresa_instance.save()
                        supervisor_instance.save()
                        practica_instance.save()

            if (recarga == True) and (vuelta == archivos_instances.count()):
                fase_practica_instance.cambio_estado(fase_practica_instance)
                practica_instance.estado_actual()

                return redirect('listaPractica', pk=practica_id)


        return render(request, self.template_name, {'estudiante_instance':estudiante_instance, 'form_practica': form_practica, 'form_fasePractica': form_fasePractica, 'form_archivo': formset, 'archivos_instances':archivos_instances, 'formset': formset,'form_empresa': form_empresa,
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
        context['estudiante_instance'] = estudiante_instance

        return context