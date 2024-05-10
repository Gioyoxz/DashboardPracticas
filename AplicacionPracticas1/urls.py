from django.contrib import admin
from django.urls import *
from django.urls import path
from AplicacionPracticas1.views import __init__
from AplicacionPracticas1.views import panel_especifico_views
from AplicacionPracticas1.views import panel_general_views
from AplicacionPracticas1.views import panel_kpis_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', panel_general_views.listaEstudiantePractica.as_view(), name="index"),
    path('kpis', panel_kpis_views.listaKPIS.as_view(), name="kpis"),
    path('practica/<pk>/', panel_especifico_views.listaPractica.as_view(), name="listaPractica"),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('cambiar_condicion/<int:practica_id>/<str:nueva_condicion>/', __init__.cambiar_condicion, name='cambiar_condicion'),

]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)