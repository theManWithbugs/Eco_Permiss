from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from functools import wraps

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
