from core.models import *
from django import forms

class RegUgaiForm(forms.ModelForm):
  class Meta:
    model = Ugai
    fields = "__all__"

  def __init__(self, *args, **kwargs):
    super(RegUgaiForm, self).__init__(*args, **kwargs)
    for f in self.fields:
      self.fields[f].widget.attrs['class'] = 'form-control'
