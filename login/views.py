# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db import models
from login.forms import LoginForm, RecoveryForm, AccountForm, EmailForm
from django.contrib.auth.models import User
from ProyectoEvaluacion.models import Alumno,Profesor
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django import forms
import random


@login_required
def profesor_login(request):	
	return render_to_response('profesor_login.html',context_instance=RequestContext(request))

def recuperar_pass(request):
	info_enviado = False
	mail_existe=True
	email = ""	
	texto = ""
	pwd=""

	""" se ingresa correo """
	if request.method == "POST":
		mailForm = RecoveryForm(request.POST)
		
		""" Todo OK y hace el procedimiento de reestablecer password """
		if mailForm.is_valid():
			email = mailForm.cleaned_data['Email']			
			user=User.objects.get(email__exact=email)
			texto = ""			

			""" actualizar password"""
			c=0

			""" autogenerar password aleatorio de 8 caracteres """
			for i in range(0,8):	
				a=random.randint(0,2)
				if (a==0):
					c=random.randint(0,9)+48
				if (a==1):
					c=random.randint(0,25)+65
				if (a==2):
					c=random.randint(0,25)+97					
				pwd=pwd+str(unichr(c))
			
			""" se guarda el password en la base de datos """
			user.set_password(pwd)
			user.save()

			""" se envía el correo electrónico con la nueva contraseña """
			html_content = "<p>Usted ha solicitado recuperar su contraseña del sistema de Evaluaciones. <br> Se ruega cambiar su contraseña una vez ingresado al sistema. </p> <p> Su nueva contraseña es: <i>%s</i> </p> <p></p><p> *No reenviar a este correo*</p>"%(pwd)
			msg = EmailMultiAlternatives('Recuperacion Contraseña',html_content,'from@server.com',[email])
			msg.attach_alternative(html_content,'text/html')	
			msg.send()

			""" se envía un mensaje al template """
			ctx = {'form':mailForm, 'success': True, 'email':email}			
			return render_to_response('recuperar_pass.html',ctx, context_instance=RequestContext(request))
		
		else:
			""" correo no valido """
			ctx = {'form':mailForm, 'success': False}
			return render_to_response('recuperar_pass.html',ctx, context_instance=RequestContext(request))
		
	else:		
		""" se muestra el formulario """
		mailForm = RecoveryForm()
		ctx = {'form':mailForm, 'success': False}
		return render_to_response('recuperar_pass.html',ctx, context_instance=RequestContext(request))

@login_required
def gestionar_cuenta_contrasena(request):
	if request.method == "POST":
		accForm = AccountForm(request.POST, user=request.user)
		if accForm.is_valid():
			print 'asdasfasf'
			password = accForm.cleaned_data['Password_Antigua']
			newpwd1 = accForm.cleaned_data['Nueva_Password']
			newpwd2 = accForm.cleaned_data['Repetir_Nueva_Password']

			user = request.user
			user.set_password(newpwd1)
			user.save()
			ctx = {'form':accForm,'success':True}
			return  render_to_response('gestionar_cuenta_contrasena.html',ctx, context_instance=RequestContext(request))
		else:
			ctx = {'form':accForm,'success':False}
			return render_to_response('gestionar_cuenta_contrasena.html',ctx, context_instance=RequestContext(request))


	else:		
		accForm = AccountForm()
		ctx = {'form':accForm,'success':False}
		return render_to_response('gestionar_cuenta_contrasena.html',ctx, context_instance=RequestContext(request))


@login_required
def gestionar_cuenta_correo(request):
	correo_actual = request.user.email
	if request.method == "POST":
		accForm = EmailForm(request.POST, user=request.user)
		
		if accForm.is_valid():			
			email = accForm.cleaned_data['Email']
			request.user.email = email
			request.user.save()
			ctx = {'form':accForm,'correo':request.user.email, 'success':True}
			return render_to_response('gestionar_cuenta_correo.html',ctx,context_instance=RequestContext(request))
		else:
			ctx = {'form':accForm,'correo':correo_actual, 'success':False}
			return render_to_response('gestionar_cuenta_correo.html',ctx, context_instance=RequestContext(request))
		
	else:		
		correo_actual = request.user.email
		accForm = EmailForm(user=request.user)
		ctx = {'form':accForm,'correo':correo_actual, 'success':False}
		return render_to_response('gestionar_cuenta_correo.html',ctx, context_instance=RequestContext(request))
