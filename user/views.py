from uuid import UUID
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout
from functools import wraps
from datetime import date
from django.forms import inlineformset_factory, model_to_dict

from core.models import *

from .forms import *

from .utils import *
from core.utils import *

def dados_pessoais_required(view_func):
    #usar wraps para evitar: quebrar reverse, perder o nome da view, quebrar permissões e logs
    @wraps(view_func)
    #quando alguém acessar essa URL, execute o wrapper primeiro
    def wrapper(request, *args, **kwargs):

        if not DadosPessoais.objects.filter(
            usuario=request.user.id
        ).exists():
            return redirect('user:dados_pss')

        #Caso o if não seja executado retorna o objeto request e os parametros da view
        #return view_func(request) → executa a view
        #A view só roda se o wrapper permitir
        return view_func(request, *args, **kwargs)

    return wrapper

def logoutView(request):
    auth_logout(request)
    return redirect('user:login')

def login_view(request):
  template_name = 'user/auth/login.html'
  if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Caso não exista vai retornar None
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                login(request, user)
                return redirect('user:home')
            except Exception as e:
                messages.error(request, f'{e}')
        else:
            messages.error(request, 'Login ou senha incorretos!')

  return render(request, template_name)

@login_required
def perfil(request):
    template_name = 'user/auth/perfil.html'

    user = get_object_or_404(DadosPessoais, usuario=request.user.id)

    context = {
        'user': user
    }

    return render(request, template_name, context)

@login_required
def dados_pessoais(request):
    template_name = 'user/auth/dados_pss.html'

    form = DadosPssForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()
            messages.success(request, "Dados pessoais registrados!")
            return redirect('user:dados_pss')
        else:
            messages.error(request, f"Erros: {form.errors}")
    else:
        form = DadosPssForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)

@login_required
def editar_dados_pss(request):
    template_name = 'user/auth/editar_dados.html'

    obj = get_object_or_404(DadosPessoais, usuario=request.user.id)

    form = DadosPssForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados alterados com sucesso!')
            return redirect('user:perfil')
        else:
            messages.error(request, f"Erros: {form.errors}")
    else:
        form = DadosPssForm(instance=obj)

    context = {
        'form': form
    }

    return render(request, template_name, context)

@login_required
def home(request):
    template_name = 'user/commons/home.html'
    return render(request, template_name)

@login_required
@dados_pessoais_required
def realizar_solic(request):
    template_name = 'user/include/realizar_solic.html'

    # dados_user = DadosPessoais.objects.filter(usuario=request.user).first()
    dados_user = get_object_or_404(DadosPessoais, usuario=request.user)

    MembroEquipeFormset = inlineformset_factory(
            DadosSolicPesquisa, MembroEquipe, form=MembroEquipeForm,
            extra=1, can_delete=True
        )

    #Declaração de variaveis locais
    prefix = 'membros'
    form_solic = DadosPesqForm()
    formset = MembroEquipeFormset(prefix=prefix)
    form_ugai = Solic_Ugai()

    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'solic_pesq':
            user = request.user

            # POST
            form_solic = DadosPesqForm(request.POST)
            if form_solic.is_valid():
                obj_paiSaved = form_solic.save(commit=False)
                obj_paiSaved.user_solic = user
                obj_paiSaved.save()

                formset = MembroEquipeFormset(request.POST, instance=obj_paiSaved, prefix=prefix)

                if formset.is_valid():
                    try:
                        formset.save()
                        messages.success(request, 'Pesquisa solicitada com sucesso!')

                        data = format_data_br(str(obj_paiSaved.data_solicitacao))
                        username = request.user.username
                        acao_realizada = obj_paiSaved.acao_realizada

                        email_solic_ugai(request, username, acao_realizada, data)
                        return redirect('user:realizar_solic')
                    except Exception as e:
                        messages.error(request, f'ocorreu um erro: {e}')
                else:
                    messages.error(request, f"Erro: {formset.errors}")
            else:
                formset = MembroEquipeFormset(request.POST, prefix=prefix)

        elif form_type == 'aut_ugai':
            form_ugai = Solic_Ugai(request.POST or None)

            user = request.user

            if form_ugai.is_valid():
                obj = form_ugai.save(commit=False)
                id_ugai = obj.id
                obj.user_solic = user
                try:
                    obj.save()
                    messages.success(request, 'Solicitação efetuada com sucesso!')

                    data_hoje = date.today()
                    data_br = data_hoje.strftime('%d/%m/%Y')

                    username = request.user.username
                    ativ_desenv = obj.ativ_desenv

                    email_solic_ugai(request, username, ativ_desenv, data_br)
                    return redirect('user:realizar_solic')
                except Exception as e:
                    messages.error(request, f'ocorreu um erro: {e}')
            else:
                messages.error(request, f"Erros: {form_ugai.errors}")

    context = {
        'form_solic': form_solic,
        'formset': formset,
        'form_ugai': form_ugai,
        'dados_user': dados_user,
    }

    return render(request, template_name, context)

@login_required
def info_pesquisa(request, id):
    template_name = 'user/include/info_pesq.html'

    try:
        id_uuid = id if isinstance(id, UUID) else UUID(str(id))
    except (ValueError, TypeError):
        return redirect("user:solic_pesq_user")

    if id_uuid != request.user.id:
        return redirect("user:solic_pesq_user")

    return render(request, template_name)

@login_required
def info_ugai(request, id):
    template_name = 'user/include/info_ugai.html'

    try:
        id_uuid = id if isinstance(id, UUID) else UUID(str(id))
    except (ValueError, TypeError):
        return redirect("user:solic_ugai_user")

    if id_uuid != request.user.id:
        return redirect("user:solic_ugai_user")

    return render(request, template_name)

@login_required
def minhas_solic_pesq(request):
    template_name = 'user/include/minhas_solic_pesq.html'
    return render(request, template_name)

@login_required
def minhas_solic_ugai(request):
    template_name = 'user/include/minhas_solic_ugai.html'
    return render(request, template_name)

def api_minhas_solic(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    objs = DadosSolicPesquisa.objects.filter(user_solic=request.user.id)

    itens_json = []
    for item in objs:
        d = model_to_dict(item)
        d['id'] = str(item.id)
        itens_json.append(d)

    return JsonResponse({
        'objs': itens_json[:10]
    })

def api_minhas_solic_ugai(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    objs = SolicitacaoUgais.objects.filter(user_solic=request.user.id)

    itens_json = []
    for item in objs:
        d = model_to_dict(item)
        d['id'] = str(item.id)
        itens_json.append(d)

    return JsonResponse({
        'objs': itens_json
    })