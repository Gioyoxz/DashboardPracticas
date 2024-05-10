from AplicacionPracticas1.views.__init__ import *

def kpis(request):

    estudiantePractica = Practica.objects.select_related('rut_persona__usuario').all()

    return render(request, 'kpis.html', {'estudiantePractica': estudiantePractica})

class listaKPIS(ListView):
    template_name = "kpis.html"
    context_object_name = "estudiantePractica"

    def get_queryset(self):

        practicaPorCarrera = Practica.objects.select_related('rut_persona__usuario').all()
        practicaPorCarrera = practicaPorCarrera.prefetch_related('empresapractica_set__rut_empresa').all()
        practicaPorCarrera = practicaPorCarrera.filter(condicion__in=['2','3','4']).all()
        practicaPorCarrera = practicaPorCarrera.order_by('estado_practica', 'conteo_practica')

        return practicaPorCarrera

    def post(self, request, *args, **kwargs):

        hoy = timezone.now().date()
        plazo_14 = hoy + timedelta(days=14)

        form_modalidad = ModalidadForm(request.POST)
        form_carrera = CarreraForm(request.POST)
        form_rubro = RubroForm(request.POST)
        form_sector = SectorForm(request.POST)
        form_tamano = TamanoForm(request.POST)
        form_buscador = BuscadorForm(request.POST)
        form_crear = CrearPracticaForm(request.POST)

        estudiantePractica = Practica.objects.select_related('rut_persona__usuario').all()
        estudiantePractica = estudiantePractica.filter(condicion__in=['2', '3', '4']).all()
        estudiantePractica = estudiantePractica.prefetch_related('empresapractica_set__rut_empresa').all()
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

        if form_modalidad.is_valid():

            modalidad_seleccionada = form_modalidad.cleaned_data['modalidad']

            if modalidad_seleccionada == '1' or modalidad_seleccionada == '2' or modalidad_seleccionada == '3':

                filtrado = filtrado.filter(modalidad=modalidad_seleccionada)

        if form_carrera.is_valid():

            carrera_seleccionada = form_carrera.cleaned_data['carrera']
            filtro_carrera = Usuario.objects.filter(carrera=carrera_seleccionada)

            if carrera_seleccionada == '1' or carrera_seleccionada == '2':

                filtrado = filtrado.filter(rut_persona__in=filtro_carrera)

        if form_rubro.is_valid():

            rubro_seleccionado = form_rubro.cleaned_data['rubro']

            if int(rubro_seleccionado) in range(1,14):

                filtrado = filtrado.filter(empresapractica__rut_empresa__rubro_empresa=rubro_seleccionado)

        if form_sector.is_valid():

            sector_seleccionado = form_sector.cleaned_data['sector']

            if sector_seleccionado == '1' or sector_seleccionado == '2' or sector_seleccionado == '3':

                filtrado = filtrado.filter(empresapractica__rut_empresa__sector=sector_seleccionado)

        if form_tamano.is_valid():

            tamano_seleccionado = form_tamano.cleaned_data['tamano']

            if tamano_seleccionado in ['1','2','3','4','5']:

                filtrado = filtrado.filter(empresapractica__rut_empresa__tamano=tamano_seleccionado)

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


        return render(request, self.template_name, {'form_buscador':form_buscador,'form_modalidad': form_modalidad,'form_carrera': form_carrera, 'form_rubro': form_rubro, 'form_sector':form_sector, 'form_tamano':form_tamano, 'form_crear': form_crear,
                                                        'estudiantePractica': filtrado, 'barra_ic': barra_ic, 'barra_iicg': barra_iicg, 'barra_fase1':barra_fase1, 'barra_fase2':barra_fase2,
                                                    'barra_fase3':barra_fase3, 'barra_fase4':barra_fase4, 'barra_fase5':barra_fase5, 'barra_vencido':barra_vencido, 'barra_pendiente':barra_pendiente,
                                                    'barra_completado':barra_completado})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        practicaPorCarrera = self.get_queryset()
        practicaPorCarrera = practicaPorCarrera.filter(condicion__in=['2', '3', '4']).all()
        practicaPorCarrera = practicaPorCarrera.prefetch_related('empresapractica_set__rut_empresa').all()
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

        context['form_modalidad'] = ModalidadForm()
        context['form_carrera'] = CarreraForm()
        context['form_rubro'] = RubroForm()
        context['form_sector'] = SectorForm()
        context['form_tamano'] = TamanoForm()
        context['form_buscador'] = BuscadorForm()
        context['form_crear'] = CrearPracticaForm

        return context