from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.forms import model_to_dict
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from uuid import UUID

from django.db import transaction

#Local imports
from core.models import *
from core.utils import calcular_data

#from rest framework to use JS fetch
import json
from django.http import JsonResponse

# =========================
# SUCCESS
# =========================
def response_200(message='Operação realizada com sucesso', data=None):
    return JsonResponse({
        'message': message,
        'data': data
    }, status=200)

def response_201(message='Recurso criado com sucesso', data=None):
    return JsonResponse({
        'message': message,
        'data': data
    }, status=201)

def response_204():
    return JsonResponse({}, status=204)

# =========================
# CLIENT ERRORS
# =========================

def response_400(message='Solicitação inválida'):
    return JsonResponse({'message': message}, status=400)


def response_401(message='Usuário não autorizado'):
    return JsonResponse({'message': message}, status=401)


def response_403(message='Acesso proibido'):
    return JsonResponse({'message': message}, status=403)


def response_404(message='Recurso não encontrado'):
    return JsonResponse({'message': message}, status=404)


def response_405(message='Método não permitido'):
    return JsonResponse({'message': message}, status=405)


def response_409(message='Conflito na requisição'):
    return JsonResponse({'message': message}, status=409)


def response_422(message='Erro de validação'):
    return JsonResponse({'message': message}, status=422)


# =========================
# SERVER ERRORS
# =========================

def response_500(message='Erro interno do servidor'):
    return JsonResponse({'message': message}, status=500)


def response_503(message='Serviço temporariamente indisponível'):
    return JsonResponse({'message': message}, status=503)

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
def info_pesquisa(request, id):
  template_name = 'core/include/info_pesq_adm.html'

  obj = get_object_or_404(DadosSolicPesquisa, id=id)
  documentos = ArquivosRelFinal.objects.filter(pesquisa=obj)
  membro_equip = MembroEquipe.objects.filter(pesquisa=obj)

  inicio = obj.inicio_atividade
  final = obj.final_atividade

  if inicio and final:
    duracao_pesq = calcular_data(str(inicio), str(final))

  context = {
    'obj': obj,
    'documentos': documentos,
    'duracao_pesq': duracao_pesq,
    'membro_equip': membro_equip
  }

  return render(request, template_name, context)

@login_required
@has_permiss
def info_ugai(request, id):
  template_name = 'core/include/info_ugai.html'

  obj = get_object_or_404(SolicitacaoUgais, id=id)
  current_ugai = get_object_or_404(Ugai, id=obj.ugai.id)

  data_inicio = obj.data_inicio
  data_final = obj.data_final

  vagas = current_ugai.vagas_disponiveis(data_inicio, data_final)

  context = {
    'obj': obj,
    'vagas': vagas,
    'current_ugai': current_ugai
  }

  return render(request, template_name, context)

#Only to render
#------------------------------------------------------------------#

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

@login_required
@has_permiss
def dashboard(request):
  template_name = 'core/include/dashboard.html'
  return render(request, template_name)

#Only action
#------------------------------------------------------------------#
@login_required
@has_permiss
def excluir_arq(request, id):
  pesquisa = get_object_or_404(DadosSolicPesquisa, id=id)
  if request.method == 'POST':
    documento_id = request.POST.get('documento_id')

    if documento_id:
        try:
            arquivo = ArquivosRelFinal.objects.get(id=documento_id)
            if pesquisa:

                documentos_associados = ArquivosRelFinal.objects.filter(id=documento_id)
                for doc in documentos_associados:
                    doc.delete_documento()

            arquivo.delete_documento()

            messages.success(request, 'Arquivo Excluido com sucesso!')
        except ArquivosRelFinal.DoesNotExist:
            messages.error(request, 'Documento não encontrado!')

  return redirect('manager:info_pesquisa', id)
#------------------------------------------------------------------#


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

def aprovar_pesq(request):
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

  if request.method == 'POST':
    data = json.loads(request.body)

    obj = get_object_or_404(DadosSolicPesquisa, id=data['id'])

    gestor_resp = f"{request.user.first_name} {request.user.last_name}"

    if obj.status == False:
      try:
        obj.status = True
        obj.gestor_resp = gestor_resp
        obj.save()

        return JsonResponse({'status': 'ok', 'message': 'Aprovação realizada com sucesso!'}, status=200)

      except DadosSolicPesquisa.DoesNotExist:
        return JsonResponse({'status': 'error(404)', 'message': 'Pesquisa não encontrada!'}, status=404)

      except Exception as e:
        return JsonResponse({'status': 'error(400)', 'message':  f'Ocorreu um erro: {e}'}, status=400)
    else:
      JsonResponse({'status': 'error(403)', 'message': 'Operação não permitida'}, status=403)
  else:
    return JsonResponse({'status': 'error(405)', 'message': 'Método não permitido!'}, status=405)


def aprovar_ugai(request):

    if not request.user.is_authenticated:
        return response_401()

    if not request.user.is_staff:
        return response_403()

    if request.method != 'POST':
        return response_405()

    try:
        data = json.loads(request.body)
    except Exception:
        return response_400('JSON inválido')

    pk = data.get('id')

    if not pk:
        return response_400('ID ausente')

    try:
        pk = UUID(pk)
    except ValueError:
        return response_400('UUID inválido')

    try:
        with transaction.atomic():

            solicitacao = SolicitacaoUgais.objects.select_for_update().get(id=pk)

            ugai = solicitacao.ugai

            vagas = ugai.vagas_disponiveis(
                solicitacao.data_inicio,
                solicitacao.data_final
            )

            if solicitacao.quantidade_pessoas > vagas:
                return response_400(f"Restam apenas {vagas} vagas")

            solicitacao.clean()
            solicitacao.status = 'APROVADO'
            solicitacao.save()

            return response_200('UGAI aprovada com sucesso')

    except SolicitacaoUgais.DoesNotExist:
        return response_404('Solicitação não encontrada')

    except Exception as e:
        return response_500(str(e))