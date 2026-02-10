from django.urls import path
from user import views
from user.views import *

app_name = "user"

urlpatterns = [
  #Current User
  #-----------------------------------------------------------------------#
  path('', views.login_view, name='login'),
  path('logout/', views.logoutView, name='logout'),

  path('perfil/', views.perfil, name='perfil'),
  path('dados_pss/', views.dados_pessoais, name='dados_pss'),
  path('editar_dados/', views.editar_dados_pss, name='editar_dados'),
  #-----------------------------------------------------------------------#

  #-----------------------------------------------------------------------#
  path('solicitar/', views.realizar_solic, name='realizar_solic'),

  #Renderizar solicitações de pesquisa
  path('minhas_solic_pesq/', views.minhas_solic_pesq, name='solic_pesq_user'),

  #Renderizar solicitações de ugai
  path('minhas_solic_ugai/', views.minhas_solic_ugai, name='solic_ugai_user'),

  path('info_pesquisas/<str:id>/', views.info_pesquisa, name='info_pesq'),
  path('info_ugai/<str:id>/', views.info_ugai, name='info_ugai'),
  #-----------------------------------------------------------------------#
  path('home/', views.home, name='home'),

  #Json responses
  path('get_my_solic_pesq/', views.api_minhas_solic, name='get_my_solic'),
  path('get_my_solic_ugai/', views.api_minhas_solic_ugai, name='get_solic_ugai')
]