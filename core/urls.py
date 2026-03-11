from django.urls import path
from core import views
from core.views import *

app_name = "manager"

urlpatterns = [
  path('login/', views.login_as_manager, name='login'),
  path('logout/', views.logoutView, name='logout'),
  path('home/', views.home, name='home'),

  path('listar_pesq/', views.listar_pesq, name='listar_pesq'),
  path('listar_ugais/', views.listar_ugais, name='listar_ugais'),

  path('info_pesq/<uuid:id>/', views.info_pesquisa, name='info_pesquisa'),
  path('info_ugai/<uuid:id>/', views.info_ugai, name='info_ugai'),

  #Default django, using template, view, model
  path('dashboard/', views.dashboard, name='dashboard'),
  path('reg_ugai/', views.reg_ugai, name='reg_ugai'),
  # path('current_data_ugais/', views.current_data_ugais, name='data_ugais'),

  path('dados_ugai/<uuid:id>/', views.dados_ugai, name='dados_ugai'),

  #Only action
  #---------------------------------------------------------#
  path('excluir_arq/<uuid:id>/', views.excluir_arq, name='excluir_arq'),
  #---------------------------------------------------------#

  #Endpoints above here
  #---------------------------------------------------------#
  path('api_resp_pesq/', views.resp_list_pesq, name='resp_pesq'),
  path('api_resp_ugai/', views.resp_list_ugai, name='resp_ugai'),

  path('api_aprovar_pesq/', views.aprovar_pesq, name='aprovar_pesq'),
  path('api_recusar_pesq/', views.recusar_pesquisa, name='recusar_pesq'),

  #Handle UGAIS
  path('api_aprovar_ugai/', views.aprovar_ugai, name='aprovar_ugai'),
  path('api_recusar_uso_ugai/', views.recusar_uso_ugai, name='negar_uso_ugai'),

  path('api_data_ugais/', views.current_data_ugais, name='data_ugais')
]
