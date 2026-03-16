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
from core.utils import calcular_data

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

@login_required
def home(request):
    template_name = 'user/commons/home.html'

    return render(request, template_name)

def login_view(request):
  template_name = 'user/auth/login.html'

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    next_url = request.POST.get('next')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        try:
          login(request, user)

          #this can be come as boolean or str
          if next_url and next_url != "None":
            return redirect(next_url)

          return redirect('user:home')

        except Exception as e:
          messages.error(request, f'{e}')
    else:
      messages.error(request, 'Login ou senha incorretos')

  next_url = request.GET.get('next')

  return render(request, template_name, {'next': next_url})

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
@dados_pessoais_required
def realizar_solic(request):
    template_name = 'user/include/realizar_solic.html'

    dados_user = get_object_or_404(DadosPessoais, usuario=request.user)

    email_to_send = DadosPessoais.objects.filter(usuario=request.user).first().email
    username = request.user.username

    MembroEquipeFormset = inlineformset_factory(
        DadosSolicPesquisa, MembroEquipe, form=MembroEquipeForm,
        extra=1, can_delete=True
    )

    prefix = 'membros'
    form_solic = DadosPesqForm()
    formset = MembroEquipeFormset(prefix=prefix)
    form_ugai = Solic_Ugai()

    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'solic_pesq':
            user = request.user
            form_solic = DadosPesqForm(request.POST)
            if form_solic.is_valid():
                obj_paiSaved = form_solic.save(commit=False)
                obj_paiSaved.user_solic = user
                obj_paiSaved.status = 'PENDENTE'
                obj_paiSaved.save()

                formset = MembroEquipeFormset(request.POST, instance=obj_paiSaved, prefix=prefix)
                if formset.is_valid():
                    try:
                        formset.save()
                        messages.success(request, 'Pesquisa solicitada com sucesso!')

                        data = format_data_br(str(obj_paiSaved.data_solicitacao))

                        acao_realizada = obj_paiSaved.acao_realizada

                        #To send email
                        esquipe = MembroEquipe.objects.filter(pesquisa=obj_paiSaved.id)
                        for x in esquipe: email_equipe_pesq(x.email, user, x.token_confirmacao)
                        esquipe.update(email_enviado=True)

                        email_solic_pesquisa(email_to_send, username, acao_realizada, data)
                        return redirect('user:realizar_solic')
                    except Exception as e:
                        messages.error(request, f'Ocorreu um erro ao salvar os membros: {e}')
                else:
                    messages.error(request, f"Erro nos membros: {formset.errors}")
            else:
                # Se o form principal não for válido, reexibe o formset vazio
                formset = MembroEquipeFormset(request.POST, prefix=prefix)
                messages.error(request, f"Erro no formulário principal: {form_solic.errors}")

        elif form_type == 'aut_ugai':
            form_ugai = Solic_Ugai(request.POST)
            user = request.user
            if form_ugai.is_valid():
                obj = form_ugai.save(commit=False)
                obj.user_solic = user
                obj.status = 'PENDENTE'
                try:
                    obj.save()
                    messages.success(request, 'Solicitação efetuada com sucesso!')

                    data_hoje = date.today()
                    data_br = data_hoje.strftime('%d/%m/%Y')

                    ativ_desenv = obj.ativ_desenv

                    email_solic_ugai(email_to_send, username, ativ_desenv, data_br)
                    return redirect('user:realizar_solic')
                except Exception as e:
                    messages.error(request, f'Ocorreu um erro ao salvar a solicitação UGAI: {e}')
            else:
                messages.error(request, f"Erros no formulário UGAI: {form_ugai.errors}")

    context = {
        'form_solic': form_solic,
        'formset': formset,
        'form_ugai': form_ugai,
        'dados_user': dados_user,
    }

    return render(request, template_name, context)

def confirm_email_equip(request, token):
    template_name = 'user/include/aut_equip.html'

    obj = get_object_or_404(MembroEquipe, token_confirmacao=token)

    # Já confirmado — não permite reprocessar
    if obj.confirmado:
        # messages.info(request, "Você já confirmou sua participação anteriormente.")
        return render(request, template_name, {'obj': obj, 'token': token, 'ja_confirmado': True})

    if request.method == "POST":
        rg_digitado = request.POST.get('rg', '').strip().upper()

        if rg_digitado == obj.rg:
            obj.confirmar()
            messages.success(request, "Participação confirmada com sucesso!")
            return redirect('user:confirm_email_equip', token=token)
        else:
            messages.error(request, "RG inválido. Tente novamente.")
            return redirect('user:confirm_email_equip', token=token)

    context = {
        'obj': obj,
        'token': token,
        'ja_confirmado': False,
    }

    return render(request, template_name, context)

@login_required
def info_pesquisa(request, id):
    template_name = 'user/include/info_pesq.html'

    try:
        UUID(str(id))
    except (ValueError, TypeError):
        messages.error(request, "Erro de segurança acesso negado!")
        return redirect("user:solic_pesq_user")

    obj = DadosSolicPesquisa.objects.filter(id=id)
    documentos = ArquivosRelFinal.objects.filter(pesquisa=obj.first())
    membro_equip = MembroEquipe.objects.filter(pesquisa=obj.first())

    obj_ = get_object_or_404(DadosSolicPesquisa, id=id)
    if obj_.user_solic.id != request.user.id:
        messages.error(request, "Você não tem permissão para acessar esta informação")
        return redirect('user:solic_pesq_user')

    form = Arq_Rel_Form(request.POST or None, request.FILES or None)

    for x in obj:
        inicio = x.inicio_atividade
        final = x.final_atividade

    if inicio and final:
        duracao_pesq = calcular_data(str(inicio), str(final))

    if request.method == 'POST':
        if form.is_valid():
            arq_pesquisa = form.save(commit=False)
            arq_pesquisa.pesquisa = obj.first()

            caminho_doc = str(arq_pesquisa.documento)
            caminho_doc = caminho_doc.split('.')
            doc_type = caminho_doc[-1]

            if doc_type != 'pdf':
                messages.error(request, 'Arquivos aceitos apenas em formato pdf!')
                return redirect('info_pesquisa', id)

            #Salva o arquivo
            arq_pesquisa.save()

            messages.success(request, 'Arquivo anexado com sucesso!')
            return redirect('user:info_pesq', id)
        else:
            messages.error(request, 'Erro ao tentar salvar!')

    context = {
        'obj': obj,
        'documentos': documentos,
        'duracao_pesq': duracao_pesq,
        'membro_equip': membro_equip,
    }

    return render(request, template_name, context)

#Only action
@login_required
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

    return redirect('user:info_pesq', id)

@login_required
def info_ugai(request, id):
    template_name = 'user/include/info_ugai.html'

    #Tem que mudar isso!
    try:
        UUID(str(id))
    except (ValueError, TypeError):
        messages.error(request, "Erro de segurança acesso negado!")
        return redirect("user:solic_ugai_user")

    solic_ugai = get_object_or_404(SolicitacaoUgais, id=id)
    if solic_ugai.user_solic.id != request.user.id:
        messages.error(request, "Você não tem permissão para acessar esta informação")
        return redirect('user:solic_ugai_user')

    context = {
        'obj': solic_ugai
    }

    return render(request, template_name, context)

@login_required
def minhas_solic_pesq(request):
    template_name = 'user/include/minhas_solic_pesq.html'
    return render(request, template_name)

@login_required
def minhas_solic_ugai(request):
    template_name = 'user/include/minhas_solic_ugai.html'
    return render(request, template_name)

#API Views
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