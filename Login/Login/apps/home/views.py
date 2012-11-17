from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db import models
from Login.apps.home.forms import LoginForm, RecoveryForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

def index_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return render_to_response('home/profesor_login.html', context_instance=RequestContext(request))
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username = username, password = password)
				if usuario is not None and usuario.is_authenticated:
					login(request, usuario)
					return render_to_response('home/profesor_login.html', context_instance=RequestContext(request))
				else:
					mensaje = "Usuario y/o Password incorrecto"
		form = LoginForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render_to_response('home/index.html', ctx, context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def profesor_view(request):
	return render_to_response('home/profesor_login.html', ctx, context_instance=RequestContext(request))

def recover_view(request):
	return render_to_response('home/recuperar_pass.html', context_instance=RequestContext(request))

def account_view(request):
	return render_to_response('home/gestionar_cuenta.html', context_instance=RequestContext(request))

def subjects_view(request):
	return render_to_response('home/ver_asignaturas.html', context_instance=RequestContext(request))

def subject1_view(request):
	return render_to_response('home/asignatura1.html', context_instance=RequestContext(request))

def evaluation1_view(request):
	return render_to_response('home/evaluation1.html', context_instance=RequestContext(request))

def distribution1_view(request):
	return render_to_response('home/distribution1.html', context_instance=RequestContext(request))

def add_student1_view(request):
	return render_to_response('home/buscar_alumno.html', context_instance=RequestContext(request))
