from .choices import *
from .utils import check_number, validador_cpf
from django.contrib.auth.models import AbstractUser
import os

from django.db import models
from django.utils import timezone
import uuid


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )


class DadosPessoais(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='usuario')
    nome = models.CharField(blank=False, null=False, max_length=80, verbose_name='Nome completo:')
    sexo = models.CharField(choices=SEXO, blank=False, null=False, max_length=10)
    estado = models.CharField(
        choices=ESTADOS_BRASIL_CHOICES, blank=False, null=False, max_length=20)
    municipio = models.CharField(blank=False, null=False, max_length=30)
    endereco = models.CharField(
        blank=False, null=False, max_length=120, verbose_name='Endereço')
    celular = models.CharField(blank=False, null=False, validators=[
                               check_number], max_length=13)
    rg = models.CharField(blank=False, null=False,
                          max_length=11, verbose_name='RG')
    org_emiss = models.CharField(
        blank=False, null=False, max_length=30, verbose_name='Orgão emissor(RG)')
    cpf = models.CharField(blank=False, null=False, validators=[
                           validador_cpf], max_length=11, verbose_name='CPF')
    telefone_fixo = models.CharField(blank=True, null=True, max_length=8, default='NA')

    cep = models.CharField(blank=False, null=False,
                           max_length=8, verbose_name='CEP')
    profis = models.CharField(blank=False, null=False,
                              max_length=30, verbose_name='Profissão/Ocupação')
    email = models.CharField(blank=True, null=True,
                             default='NA', max_length=80)

    def __str__(self):
        return f"{self.nome}"

    def save(self, *args, **kwargs):
        # Itera sobre todos os campos do modelo
        for field in self._meta.fields:
            value = getattr(self, field.name)

            if (
                isinstance(field, models.CharField) and
                value is not None and
                field.name != "email"
            ):
                setattr(self, field.name, value.upper())

        super().save(*args, **kwargs)

    class Meta:
        db_table = "dados_pessoais"


class DadosSolicPesquisa(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_solic = models.ForeignKey(User, on_delete=models.CASCADE)

    data_solicitacao = models.DateField(default=timezone.localdate)

    acao_realizada = models.CharField(
        blank=False, null=False, max_length=80, verbose_name='Qual atividade será realizada na UC?')

    # I can't understand, this field needs attention!
    unidade_cons = models.CharField(blank=False, null=False, max_length=80,
                                    verbose_name='Unidade(s) de conservação onde será(ão) realizada(s) a atividade')

    tipo_solic = models.CharField(
        choices=TIPO_SOLIC, blank=False, null=False, verbose_name='Tipo de solicitação', max_length=20)

    foto = models.CharField(choices=YES_OR_NOT, blank=False,
                            null=False, verbose_name='Fotografia e imagens da UC?', max_length=3)

    licenca_inst = models.CharField(
        choices=YES_OR_NOT, blank=False, null=False, verbose_name='Licença de instituição responsavel?', max_length=3)

    inicio_atividade = models.DateField(default=timezone.localdate)
    final_atividade = models.DateField(default=timezone.localdate)

    retorno_comuni = models.CharField(
        choices=YES_OR_NOT, blank=False, null=False, verbose_name='Retorno para a comunidade', max_length=3)

    area_atuacao = models.CharField(
        choices=CHOICES_AREA_ATUACAO, blank=False, null=False, verbose_name='Aréa de atuação', max_length=100)

    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.data_solicitacao}"

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if isinstance(field, models.CharField) and value is not None:
                setattr(self, field.name, value.upper())
        super().save(*args, **kwargs)

    class Meta:
        db_table = "solic_pesquisa"

class MembroEquipe(models.Model):
    pesquisa = models.ForeignKey(
        DadosSolicPesquisa, on_delete=models.CASCADE, related_name='pesquisa')
    nome = models.CharField(blank=False, null=False, max_length=80)
    rg = models.CharField(blank=False, null=False,
                          max_length=11, verbose_name='RG')
    cpf = models.CharField(blank=False, null=False, validators=[
                           validador_cpf], max_length=11, verbose_name='CPF')
    instituicao = models.CharField(
        blank=False, null=False, verbose_name='Instiuições', max_length=80)

    def __str__(self):
        return f"{self.nome}"

def get_upload_path(instance, filename):
    ano = timezone.now().year
    area_atuacao = instance.pesquisa.area_atuacao

    return os.path.join('rel_final_pesq', str(ano), str(area_atuacao), filename)

class ArquivosRelFinal(models.Model):
    pesquisa = models.ForeignKey(
        DadosSolicPesquisa, on_delete=models.CASCADE, related_name='arq_pesquisa')
    documento = models.FileField(upload_to=get_upload_path)
    upado_em = models.DateTimeField(default=timezone.now)

    def delete_documento(self):
        if self.documento:
            if os.path.isfile(self.documento.path):
                os.remove(self.documento.path)
            self.documento = None
        self.delete()

    def __str__(self):
        return f"{self.pesquisa.acao_realizada}"

class SolicitacaoUgais(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_solic = models.ForeignKey(User, on_delete=models.CASCADE)
    ugai = models.CharField(choices=CHOICES_UGAIS, max_length=16, verbose_name='Qual ugai?')
    instituicao = models.CharField(max_length=40, blank=True, null=True, verbose_name='Instituição', default='NA')
    setor = models.CharField(max_length=40, blank=True, null=True, default='NA')
    cargo = models.CharField(max_length=40, blank=True, null=True, default='NA')
    ativ_desenv = models.CharField(max_length=80, blank=False, null=False, verbose_name='Atividades que irá desenvolver')
    publico_alvo = models.CharField(max_length=80, blank=False, null=False, verbose_name='Público alvo')
    status = models.BooleanField(default=False)
    data_solicitacao = models.DateField(default=timezone.localdate)
    data_inicio = models.DateField(default=timezone.localdate)
    data_final = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.ugai}"

    class Meta:
        db_table = "solic_ugai"