# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db import models
from Login.apps.home.forms import LoginForm, RecoveryForm, AccountForm
from django.contrib.auth.models import User
from Login.apps.home.models import Alumno, Usuario
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
import random
#k.klingenberg@gmail.com
logged_user=""
def index_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return render_to_response('home/profesor_login.html', context_instance=RequestContext(request))
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				logged_user=username
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
	mail_existe=True
	email = ""	
	texto = ""
	pwd=""
	if request.method == "POST":
		mailForm = RecoveryForm(request.POST)
		if mailForm.is_valid():
			
			email = mailForm.cleaned_data['Email']			
			texto = ""			
			""" actualizar password"""
			#usr=User();
			try:
				user=User.objects.get(email__exact=email)
				#user=Alumno.objects.get(email__exact=email)
			except Exception:
				mail_existe=False
			
			if (mail_existe):	
				""" Todo OK y hace el procedimiento de reestablecer password """
				info_enviado = True
				mail_existe=True
				c=0
				""" autogenerar password aleatorio de 8 caracteres """
				for i in range(0,8):	
					a=random.randint(0,2)
					if (a==0): #caso para crear enteros
						c=random.randint(0,9)+48
					if (a==1): #caso para crear caracteres mayusculas
						c=random.randint(0,25)+65
					if (a==2): #caso para crear caracteres minusculas
						c=random.randint(0,25)+97					
					pwd=pwd+str(unichr(c))
				
				user.set_password(pwd)
				user.save()
				html_content = "Hola. Esto es la recuperacion de contrasegna. Se ruega cambiar su contrasegna una vez ingresado al sistema. <br> Su nueva contrasegna es :%s <br><br><br> *No reenviar a este correo*<br>"%(pwd)
				msg = EmailMultiAlternatives('Recuperacion Contrasegna',html_content,'from@server.com',[email])
				msg.attach_alternative(html_content,'text/html')
				ctx = {'form':mailForm, 'email':email,'info_enviado':info_enviado,'pass':pwd,'mail_existe':mail_existe}				
				msg.send()
				return render_to_response('home/recuperar_pass.html',ctx,context_instance=RequestContext(request))
			else:
				info_enviado=False
				ctx = {'form':mailForm, 'email':email,'info_enviado':info_enviado,'pass':pwd,'mail_existe':mail_existe}
				return render_to_response('home/recuperar_pass.html',ctx,context_instance=RequestContext(request))
		else:			
			info_enviado=False
			mail_existe=False
			ctx = {'form':mailForm, 'email':email,'info_enviado':info_enviado,'mail_existe':mail_existe}
			return render_to_response('home/recuperar_pass.html',ctx, context_instance=RequestContext(request))
		
	else:		
		mailForm = RecoveryForm()
		ctx = {'form':mailForm, 'email':email,'texto':texto,'mail_existe':mail_existe, 'info_enviado':info_enviado}
		return render_to_response('home/recuperar_pass.html',ctx, context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def account_view(request):
	email = ""	
	texto = ""
	if request.method == "POST":
		accForm = AccountForm(request.POST)
		
		if accForm.is_valid():			
			email = accForm.cleaned_data['Correo_Electronico']
			password = accForm.cleaned_data['Password_Antigua']
			newpwd1 = accForm.cleaned_data['Nueva_Password']
			newpwd2 = accForm.cleaned_data['Repetir_Nueva_Password']

# ARREGLAR ESTO, FALTAN VALIDACIONES, VERIFICAR POR RUT Y NO POR EMAIL SOLAMENTE
#    EJ. SI EMAIL NO EXISTE, ESE MAIL PASA A SER DEL USUARIO.

			if newpwd1 == newpwd2:				
				try:
					user=User.objects.get(email__exact=email)
					#user=Alumno.objects.get(email__exact=email)
					if (user.username == logged_user):
						if user.check_password(password):
							""" Todo OK y hace el procedimiento de cambiar password """
							user.set_password(newpwd1)
							user.save()
							texto="Información guardada satisfactoriamente."
							ctx = {'form':accForm, 'texto':texto}
							return render_to_response('home/gestionar_cuenta.html',ctx,context_instance=RequestContext(request))
						else:
							texto="Password antigua no coincide."
							ctx = {'form':accForm, 'texto':texto}
							return render_to_response('home/gestionar_cuenta.html',ctx,context_instance=RequestContext(request))
					else:
						texto = "Email ya fue usado."
						ctx = {'form':accForm, 'texto':texto}
						return render_to_response('home/gestionar_cuenta.html',ctx,context_instance=RequestContext(request))

				except Exception:					
					texto="Correo no Existe."
					ctx = {'form':accForm, 'texto':texto}
					return render_to_response('home/gestionar_cuenta.html',ctx,context_instance=RequestContext(request))
		
			else: 
				texto="Password nueva no coincide."
				ctx = {'form':accForm, 'texto':texto}
				return render_to_response('home/gestionar_cuenta.html',ctx,context_instance=RequestContext(request))

		else:
			texto="Correo no válido."
			ctx = {'form':accForm, 'texto':texto}
			return render_to_response('home/gestionar_cuenta.html',ctx, context_instance=RequestContext(request))
		
	else:		
		accForm = AccountForm()
		ctx = {'form':accForm, 'texto':texto}
		return render_to_response('home/gestionar_cuenta.html',ctx, context_instance=RequestContext(request))


@login_required(redirect_field_name='/ingresar')
def subjects_view(request):
	usr = Usuario(rut="44444444-4",username="Flan3", nombre="Flan3", email="adsf@asdf.com", password="qwerty2", tipo = "PR")
	#print(alum)
	#alum=alumno.objects.create(id_alumno=1,rut='8093585-4',nombre='Luis Diaz',email='luisediazt.58@gmail.com','8093585')
	#usr.save()
	ctx = '' #{'alumno': usr}
	return render_to_response('home/ver_asignaturas.html',ctx ,context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def subject1_view(request):
	return render_to_response('home/asignatura1.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def evaluation1_view(request):
	return render_to_response('home/evaluation1.html', context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def distribution1_view(request):
	usr = User.objects.all()
	#usr = Alumno.objects.all()
	valores =range(1,len(usr)+1)
	ctx = {'usr': usr, 'range':range(1,9), 'valores':valores}
	return render_to_response('home/distribution1.html', ctx, context_instance=RequestContext(request))

@login_required(redirect_field_name='/ingresar')
def add_student1_view(request):
	return render_to_response('home/buscar_alumno.html', context_instance=RequestContext(request))


"""
NO SABEMOS EDITAR UNA Password A PARTIR DEL ADMINISTRADOR DE django

"""
