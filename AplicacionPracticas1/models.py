from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from numpy import busday_count
from django.utils import timezone
from datetime import timedelta
from multiupload.fields import MultiFileField
from django.core.exceptions import ObjectDoesNotExist


class Persona(models.Model):
    rut_persona = models.CharField('Rut o Dni', max_length=12, null=False, blank=False, primary_key=True,
                                   help_text='Ingrese Rut o Dni sin puntos ni guión')
    nombre_persona = models.CharField('Nombre', max_length=50, null=False, blank=False)
    correo_persona = models.CharField('Correo', max_length=40, null=False, blank=False)
    telefono_persona = PhoneNumberField('Telefono', blank=True, help_text="+569XXXXXX")

    def Persona(self):
        return "{} | {} | {} | {}".format(self.rut_persona, self.nombre_persona, self.correo_persona,
                                          self.telefono_persona)

    def __str__(self):
        return self.Persona()

    class Meta:
        pass


class Carrera(models.Model):
    carreras = (("1", "IC"), ("2", "IICG"))
    carrera = models.CharField(max_length=50, null=False, blank=True, choices=carreras)

    def Carrera(self):
        return "{}".format(self.get_carrera_display())

    def __str__(self):
        return self.Carrera()


class Usuario(Persona):
    contrasena = models.CharField('Contraseña', max_length=50, null=False, blank=False)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def Usuario(self):
        return "{} | {}".format(self.rut_persona, self.contrasena)

    def __str__(self):
        return self.Usuario()


class Empresa(models.Model):
    rut_empresa = models.CharField('Rut', max_length=12, null=False, blank=False, primary_key=True,
                                   help_text='(Sin puntos ni guión)')
    nombre_empresa = models.CharField('Nombre', max_length=50, null=False, blank=False)
    rubro_empresa = models.CharField('Rubro', max_length=50, null=False, blank=False)

    def Empresa(self):
        return "{} | {} | {}".format(self.rut_empresa, self.nombre_empresa, self.rubro_empresa)

    def __str__(self):
        return self.Empresa()


class Fase(models.Model):
    fases = (("1", "Inscripción"), ("2", "Inicio"), ("3", "Término"), ("4", "Informe"), ("5", "Evaluación"))  # Falta dividir en más fases
    fase = models.CharField("Fase de", max_length=50, null=False, blank=True, choices=fases)

    def Fase(self):
        return "{}".format(self.get_fase_display())

    def __str__(self):
        return self.Fase()


class Documento(models.Model):
    verificacion = models.BooleanField(default=False)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, null=True)

    def Documento(self):
        return "{} | {}".format(self.verificacion, self.fase)

    def __str__(self):
        return self.Documento()


class Practica(models.Model):
    rut_persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True)

    id_practica = models.AutoField(primary_key=True)
    fechaCreación = models.DateField('Fecha de Creación', max_length=50, null=True, blank=False)
    fechaInicio = models.DateField('Fecha de Inicio', max_length=50, null=True, blank=False)
    fechaFin = models.DateField('Fecha de Fin', max_length=30, null=True, blank=False)
    condiciones = (("1", "Cursando"), ("2", "Cancelado"), ("3", "Aprobado"), ("4", "Rechazado"))
    condicion = models.CharField("Estado", default='1', choices=condiciones)
    estados = (("1", "Pendiente"), ("2", "Completado"), ("3", "Vencido"))
    estado_practica = models.CharField("Estado", default='2', choices=estados)
    conteo_practica = models.IntegerField('Conteo', null=True)
    horas = models.IntegerField('Horas', null=True, blank=False)
    observacion = models.CharField('Observación', max_length=50, null=True, blank=False)

    fase_actual = models.ForeignKey(Fase, on_delete=models.SET_NULL, null=True)

    def fase_ultima(self):
        fase_actual_instancia = FasePractica.objects.filter(id_practica=self.id_practica).last()
        if fase_actual_instancia:
            self.fase_actual = fase_actual_instancia.fase
            self.save()

    def estado_actual(self):
        fase_actual_instancia = FasePractica.objects.filter(id_practica=self.id_practica).last()
        if fase_actual_instancia:
            self.estado_practica = fase_actual_instancia.estado
            self.save()

    def conteo_actual(self):
        fase_actual_instancia = FasePractica.objects.filter(id_practica=self.id_practica).last()
        if fase_actual_instancia:
            self.conteo_practica = fase_actual_instancia.conteo
            self.save()

    def Practica(self):
        return "{} | {} | {} | {} | {}".format(self.fechaInicio, self.fechaFin, self.get_condicion_display(), self.horas, self.observacion)

    def __str__(self):
        return self.Practica()


class EmpresaPractica(models.Model):
    id_practica = models.ForeignKey(Practica, on_delete=models.SET_NULL, null=True)
    rut_empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)

    fecha_empresa_practica = models.DateField('Fecha', max_length=50, null=False, blank=False, auto_now_add=True)
    nombre_supervisor = models.CharField('Supervisor', max_length=30, null=True)
    correo_supervisor = models.CharField('Correo', max_length=30, null=True)
    telefono_supervisor = PhoneNumberField('Telefono', null=True, help_text="(+569XXXXXX)")

    def EmpresaPractica(self):
        return "{} | {} | {}".format(self.nombre_supervisor, self.correo_supervisor, self.telefono_supervisor)

    def __str__(self):
        return self.EmpresaPractica()

    class Meta:
        unique_together = ('rut_empresa', 'id_practica')


class FasePractica(models.Model):
    id_practica = models.ForeignKey(Practica, on_delete=models.SET_NULL, null=True)
    fase = models.ForeignKey(Fase, on_delete=models.SET_NULL, null=True)
    fecha_conteo = models.DateField('Fecha conteo', max_length=50, null=True)
    conteo = models.IntegerField('Conteo', null=True)
    estados = (("1", "Vencido"), ("2", "Pendiente"), ("3", "Completado"))
    estado = models.CharField("Estado", default='2', choices=estados)
    guardados = models.IntegerField('Guardados', null=True, default=0)

    def actualizar_contador(self):
        hoy = timezone.now().date()

        practica_instance = Practica.objects.get(id_practica=self.id_practica.id_practica)
        archivos_instances = Archivo.objects.filter(fase_practica=self).all()

        if self.fase.fase == '1':

            if practica_instance.fechaInicio != None:

                diferencia = practica_instance.fechaInicio - hoy
                self.conteo = diferencia.days

            else:

                diferencia = self.fecha_conteo - hoy
                self.conteo = diferencia.days

        elif self.fase.fase == '2':

            diferencia = practica_instance.fechaFin - hoy
            self.conteo = diferencia.days

        elif self.fase.fase == '3':

            diferencia = hoy - practica_instance.fechaFin
            self.conteo = 15 - diferencia.days

        elif self.fase.fase == '4':

            diferencia = hoy - practica_instance.fechaFin
            self.conteo = 30 - diferencia.days

        self.save()

        # Verificar si ha pasado un día desde la última actualización



    def cambio_estado(self, instancia):
        hoy = timezone.now().date()
        plazo_14 = hoy + timedelta(days=14)

        instancia_practica = Practica.objects.get(id_practica=self.id_practica.id_practica)
        relleno_practica = False
        if (instancia_practica.fechaInicio and instancia_practica.fechaFin) != (None or ""):
            relleno_practica = True
            print("relleno_practica")

        instancia_usuario = Usuario.objects.get(rut_persona=instancia_practica.rut_persona.rut_persona)
        relleno_estudiante = True

        if (instancia_usuario.nombre_persona or instancia_usuario.carrera or instancia_usuario.correo_persona or instancia_usuario.telefono_persona) == (None or ""):
            relleno_estudiante = False
            print("relleno_estudiante")

        try:
            supervisor_instancia = EmpresaPractica.objects.get(id_practica=self.id_practica)
        except ObjectDoesNotExist:
            supervisor_instancia = None

        archivo_instancias = Archivo.objects.filter(fase_practica=instancia).all()
        cambio = True


        if self.conteo > 0:

            self.estado = "2"
            self.save()

            if (supervisor_instancia != None) and ((relleno_estudiante == True) and ( relleno_practica == True)):

                print("supervisor_instancia != None")

                if archivo_instancias:

                    print("if archivo_instancias:")

                    for a in archivo_instancias:

                        print("for a in archivo_instancias:")

                        if (a.archivo == ""):
                            self.estado = "2"
                            cambio = False
                            self.save()
                            print("if (a.archivo == "")")

                else: cambio = True

                if cambio == True:
                    self.estado = "3"
                    self.save()

            if cambio == False:
                self.estado = "2"
                self.save()

        if self.conteo <= 0:

            if self.estado == '1':

                if (supervisor_instancia != None) and ((relleno_estudiante == True) and (relleno_practica == True)):

                    print("supervisor_instancia != None")

                    if archivo_instancias:

                        print("if archivo_instancias:")

                        for a in archivo_instancias:

                            print("for a in archivo_instancias:")

                            if (a.archivo == ""):
                                self.estado = "1"
                                cambio = False
                                self.save()
                                print("if (a.archivo == "")")

                    else:
                        cambio = True

                    if cambio == True:
                        self.estado = "3"
                        self.save()

                if cambio == False:
                    self.estado = "1"
                    self.save()

            if self.estado == '2':
                self.estado = '1'

            if self.estado == '3':
                siguiente_num = str(int(self.fase.fase) + 1)
                siguiente_fase = Fase.objects.get(fase=siguiente_num)

                nueva_instancia = FasePractica.objects.create(id_practica=self.id_practica, fase=siguiente_fase, conteo= 14,fecha_conteo=plazo_14)

                for doc in Documento.objects.filter(fase=siguiente_fase):
                    Archivo.objects.create(fase_practica=nueva_instancia, documento=doc)

                nueva_instancia.actualizar_contador()

        else:
            self.estado = self.estado

        self.save()

    def contar_guardados(self, archivos_instancias):

        #archivos_instancias = Archivo.objects.filter(fase_practica=instancia).all()
        conteo_guardados = 0

        for i in archivos_instancias:

            if i.archivo != None and i.archivo != "":

                conteo_guardados += 1

        self.guardados = conteo_guardados
        self.save()

    def FasePractica(self):
        return "{} | {} | {} | {}".format(self.fecha_conteo, self.conteo, self.estado, self.guardados)

    def __str__(self):
        return self.FasePractica()

    class Meta:
        unique_together = ('id_practica', 'fase')

class Documento(models.Model):
    fase = models.ForeignKey(Fase, on_delete=models.SET_NULL, null=True)
    documentos = (("1", "Formulario de Inscripción"), ("2", "Plan de Trabajo"), ("3", "Carta de Aceptación"),
                  ("4", "Carta de Compromiso"), ("5", "Constancia de Termino"),
                  ("6", "Informe de Práctica"))  # Falta dividir en más fases
    documento = models.CharField("Documento", max_length=50, null=False, blank=True, choices=documentos)

    def Documento(self):
        return "{}".format(self.get_documento_display())

    def __str__(self):
        return self.Documento()


class Archivo(models.Model):
    fase_practica = models.ForeignKey(FasePractica, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    archivo = models.FileField('', upload_to='attachments', null=True)

    def Archivo(self):
        return "{} | {}".format(self.documento.get_documento_display(), self.archivo)

    def __str__(self):
        return self.Archivo()