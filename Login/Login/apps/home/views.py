# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db import models
from Login.apps.home.forms import LoginForm, RecoveryForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
#from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import random

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

@login_required(redirect_field_name='/ingresar')
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')

@login_required(redirect_field_name='/ingresar')
def profesor_view(request):	
	return render_to_response('home/profesor_login.html', context_instance=RequestContext(request))


def recover_view(request):
	info_enviado = False
	email = ""	
	texto = ""
	if request.method == "POST":
		mailForm = RecoveryForm(request.POST)
		if mailForm.is_valid():
			info_enviado = True
			email = mailForm.cleaned_data['Email']			
			texto = ""			
			

			
			""" actualizar password"""
			#usr=User();
			user=User.objects.get(email__exact=email)	
			ps1=random.randint(100,1000)
			ps2=random.randint(100,1000)
			ps3=random.randint(100,1000)
			pwd=str(ps1)+str(ps2)+str(ps3)
			user.set_password(pwd)
			#user=User(user.password=user.username);
			#user=auth_user(user.id,user.username,user.password)
			user.save()
			html_content = "Hola. Esta es la recuperacion de contrasegna. Se ruega cambiar su contrasegna una vez ingresado al sistema. <br> Su nueva contrasegna es :%s <br><br><br> *No reenviar a este correo*<br>"%(pwd)
			msg = EmailMultiAlternatives('Recuperacion Contrasegna',html_content,'from@server.com',[email])
			msg.attach_alternative(html_content,'text/html')
			ctx = {'form':mailForm, 'email':email,'info_enviado':info_enviado,'pass':pwd}
			msg.send()
			return render_to_response('home/recuperar_pass.html',ctx,context_instance=RequestContext(request))
		else:			
			info_enviado=False
			ctx = {'form':mailForm, 'email':email,'info_enviado':info_enviado}
			return render_to_response('home/recuperar_pass.html',ctx, context_instance=RequestContext(request))
		
	else:		
		mailForm = RecoveryForm()
		ctx = {'form':mailForm, 'email':email,'texto':texto, 'info_enviado':info_enviado}
		return render_to_response('home/recuperar_pass.html',ctx, context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def account_view(request):
	return render_to_response('home/gestionar_cuenta.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def subjects_view(request):
	return render_to_response('home/ver_asignaturas.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def subject1_view(request):
	return render_to_response('home/asignatura1.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def evaluation1_view(request):
	return render_to_response('home/evaluation1.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def distribution1_view(request):
	return render_to_response('home/distribution1.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def add_student1_view(request):
	return render_to_response('home/buscar_alumno.html', context_instance=RequestContext(request))
