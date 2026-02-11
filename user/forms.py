from core.models import *
from django import forms

class DadosPssForm(forms.ModelForm):
  class Meta:
    model = DadosPessoais
    fields = "__all__"
    exclude = ['usuario']

  def __init__(self, *args, **kwargs):
    super(DadosPssForm, self).__init__(*args, **kwargs)
    for f in self.fields:
      self.fields[f].widget.attrs['class'] = 'form-control'
    self.fields['sexo'].widget.attrs.update({'class': 'form-select'})
    self.fields['estado'].widget.attrs.update({'class': 'form-select'})

class DadosPesqForm(forms.ModelForm):
  class Meta:
    model = DadosSolicPesquisa
    fields = '__all__'
    exclude = ['user_solic', 'data_solicitacao', 'status']
    widgets = {
        'rel_final': forms.Textarea(attrs={
          'class': 'form-control form-control-sm',
          'rows': 3,
        }),
      }

  def __init__(self, *args, **kwargs):
    super(DadosPesqForm, self).__init__(*args, **kwargs)
    for f in self.fields:
      self.fields[f].widget.attrs['class'] = 'form-control'
    self.fields['foto'].widget.attrs.update({'class': 'form-select'})
    self.fields['area_atuacao'].widget.attrs.update({'class': 'form-select'})
    self.fields['tipo_solic'].widget.attrs.update({'class': 'form-select'})
    self.fields['licenca_inst'].widget.attrs.update({'class': 'form-select'})
    self.fields['retorno_comuni'].widget.attrs.update({'class': 'form-select'})
    self.fields['inicio_atividade'].widget = forms.DateInput(attrs={
        'class': 'form-control form-control',
        'type': 'date',
      })
    self.fields['final_atividade'].widget = forms.DateInput(attrs={
        'class': 'form-control form-control',
        'type': 'date',
      })

class MembroEquipeForm(forms.ModelForm):
  class Meta:
    model = MembroEquipe
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(MembroEquipeForm, self).__init__(*args, **kwargs)
    for f in self.fields:
      self.fields[f].widget.attrs['class'] = 'form-control'

class Solic_Ugai(forms.ModelForm):
  class Meta:
    model = SolicitacaoUgais
    fields = '__all__'
    exclude = ['user_solic', 'data_solicitacao']
    widgets = {
      'ativ_desenv': forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 2,
        'placeholder': 'Descrição das atividades...'
      }),
    }

  def __init__(self, *args, **kwargs):
    super(Solic_Ugai, self).__init__(*args, **kwargs)
    for f in self.fields:
      self.fields[f].widget.attrs['class'] = 'form-control'
    self.fields['ugai'].widget.attrs.update({'class': 'form-select'})
    self.fields['data_inicio'].widget = forms.DateInput(attrs={
        'class': 'form-control form-control',
        'type': 'date',
      })
    self.fields['data_final'].widget = forms.DateInput(attrs={
        'class': 'form-control form-control',
        'type': 'date',
      })

class Arq_Rel_Form(forms.ModelForm):
  class Meta:
    model = ArquivosRelFinal
    fields = ['documento']

  def __init__(self, *args, **kwargs):
    super(Arq_Rel_Form, self).__init__(*args, **kwargs)
    for f in self.fields:
      self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'
      self.fields['documento'].widget.attrs['readonly'] = 'readonly'