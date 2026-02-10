from django.shortcuts import render

def login(request):
  template_name = 'core/auth/login.html'
  return render(request, template_name)
