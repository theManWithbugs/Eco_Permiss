from django.urls import path
from core import views
from core.views import *

app_name = "manager"

urlpatterns = [
  path('', views.login_as_manager, name='login'),
  path('home/', views.home, name='home'),

  path('listar_pesq/', views.listar_pesq, name='listar_pesq'),
  path('listar_ugais/', views.listar_ugais, name='listar_ugais'),

  path('info_pesq/<str:id>/', views.info_pesquisa, name='info_pesquisa'),
  path('info_ugai/<str:id>/', views.info_ugai, name='info_ugai'),

  path('dashboard/', views.dashboard, name='dashboard'),

  #Only action
  #---------------------------------------------------------#
  path('excluir_arq/<str:id>/', views.excluir_arq, name='excluir_arq'),
  #---------------------------------------------------------#

  #Endpoints above here
  #---------------------------------------------------------#
  path('api_resp_pesq/', views.resp_list_pesq, name='resp_pesq'),
  path('api_resp_ugai/', views.resp_list_ugai, name='resp_ugai'),

  path('api_aprovar_pesq/', views.aprovar_pesq, name='aprovar_pesq')
]
