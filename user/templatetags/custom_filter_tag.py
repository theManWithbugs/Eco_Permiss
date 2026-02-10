from django import template
from core.models import *

register = template.Library()

@register.filter(name="format_document")
def doc_formater(string):
  string = string.split('/')

  return string[3][:30]