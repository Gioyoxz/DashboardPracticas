
from django.contrib import admin
from django.urls import *

from django.urls import path
from AplicacionPracticas1.views import *
from AplicacionPracticas1 import views
from django.views.generic import TemplateView


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.listaEstudiantePractica.as_view(), name="index"),
    path('practica/<pk>/', views.listaPractica.as_view(), name="listaPractica"),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('cambiar_condicion/<int:practica_id>/<str:nueva_condicion>/', views.cambiar_condicion, name='cambiar_condicion'),

]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)