from django.shortcuts import render, redirect
from django.views.generic import ListView
from AplicacionPracticas1.forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.utils import timezone
from datetime import timedelta
from docx import Document
from datetime import datetime

def cambiar_condicion(request, practica_id, nueva_condicion):
    practica = Practica.objects.get(id_practica=practica_id)
    practica = practica.filter(condicion__in=['2', '3', '4']).all()
    practica.condicion = nueva_condicion
    fase_practica_instancia = FasePractica.objects.filter(id_practica=practica).last()
    fase_practica_instancia.estado = '3'
    practica.estado_practica = '3'
    fase_practica_instancia.save()
    practica.save()
    return redirect('listaPractica', pk=practica_id)