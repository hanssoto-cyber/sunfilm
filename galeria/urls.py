from django.urls import path
from . import views

app_name = 'galeria'

urlpatterns = [
    path('', views.lista, name='lista'),
]