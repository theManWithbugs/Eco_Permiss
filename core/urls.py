from django.urls import path
from core import views
from core.views import *

app_name = "manager"

urlpatterns = [
  path('', views.login_as_manager, name='login'),
  path('home/', views.home, name='home'),
]
