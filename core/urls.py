from django.urls import path
from core import views
from core.views import *

app_name = "manager"

urlpatterns = [
  path('', views.login_as_manager, name='login'),
  path('home/', views.home, name='home'),

  path('listar_pesq/', views.listar_pesq, name='listar_pesq'),

  #Endpoints above here
  #---------------------------------------------------------#
  path('api_resp_pesq/', views.resp_list_pesq, name='resp_pesq'),
]
