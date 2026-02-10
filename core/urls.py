from django.urls import path
from core import views
from core.views import *

app_name = "core"

urlpatterns = [
  path('', views.login, name='login'),
]
