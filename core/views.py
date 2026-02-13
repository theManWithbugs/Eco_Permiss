from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.forms import model_to_dict
from django.core.paginator import Paginator

#Local imports
from core.models import *

#from rest framework to use JS fetch
import json
from django.http import JsonResponse

def has_permiss(view_func):
  @wraps(view_func)
  def wrapper(request, *args, **kwargs):

    if not request.user.is_staff:
      messages.error(request, 'Permissão de acesso negada!')
      return redirect('manager:login')

    return view_func(request, *args, **kwargs)

  return wrapper

def login_as_manager(request):
  template_name = 'core/auth/login.html'
  if request.method == 'POST':
    username =  request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      if not user.is_staff:
        messages.error(request, 'Apenas gestores estão autorizados!')
        return redirect('manager:login')
      else:
        try:
          login(request, user)
          return redirect('manager:home')
        except Exception as e:
          messages.error(request, f'{e}')
    else:
      messages.error(request, 'Login ou senha incorretos!')

  return render(request, template_name)

@login_required
@has_permiss
def home(request):
  template_name = 'core/commons/home.html'
  return render(request, template_name)

@login_required
@has_permiss
def listar_pesq(request):
  template_name = 'core/include/listar_pesq.html'
  return render(request, template_name)

@login_required
@has_permiss
def listar_ugais(request):
  template_name = 'core/include/listar_ugai.html'
  return render(request, template_name)

#API endpoints
#------------------------------------------------------------------#
def resp_list_pesq(request):
  if not request.user.is_authenticated:
    return JsonResponse(
      {'error': 'Usuario não autenticado'},
      status=401
    )

  if not request.user.is_staff:
    return JsonResponse(
      {'error': 'Usuario não autorizado!'},
      status=401
    )

  status = request.GET.get('status')
  if status.lower() == "true":
    status = True
  elif status.lower() == "false":
    status = False
  else:
    return JsonResponse({'error': 'Status inválido'}, status=400)

  dados = DadosSolicPesquisa.objects.filter(status=status).order_by('-data_solicitacao')

  page_number = request.GET.get('page', 1)
  paginator = Paginator(dados, 5)

  page_number = request.GET.get('page', 1)
  page_obj = paginator.get_page(page_number)

  itens_json = []
  for item in page_obj:
    d = model_to_dict(item)
    d['id'] = str(item.id)
    itens_json.append(d)

  return JsonResponse({
    'objs': itens_json,
    'currentPage': page_obj.number,
    'totalPages': paginator.num_pages,
    'hasNext': page_obj.has_next(),
    'hasPrevious': page_obj.has_previous()
  })

def resp_list_ugai(request):
  if not request.user.is_authenticated:
    return JsonResponse(
      {'error': 'Usuario não autenticado'},
      status=401
    )

  if not request.user.is_staff:
    return JsonResponse(
      {'error': 'Usuario não autorizado!'},
      status=401
    )

  status = request.GET.get('status')
  if status.lower() == "true":
    status = True
  elif status.lower() == "false":
    status = False
  else:
    return JsonResponse({'error': 'Status inválido'}, status=400)

  dados = SolicitacaoUgais.objects.filter(status=status).order_by('-data_solicitacao')

  page_number = request.GET.get('page', 1)
  paginator = Paginator(dados, 5)

  page_number = request.GET.get('page', 1)
  page_obj = paginator.get_page(page_number)

  itens_json = []
  for item in page_obj:
    d = model_to_dict(item)
    d['id'] = str(item.id)
    itens_json.append(d)

  return JsonResponse({
    'objs': itens_json,
    'currentPage': page_obj.number,
    'totalPages': paginator.num_pages,
    'hasNext': page_obj.has_next(),
    'hasPrevious': page_obj.has_previous()
  })

  return JsonResponse({
    'message': 'isso vem do backend(Ugais)'
  })