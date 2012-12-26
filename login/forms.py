# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username	= forms.CharField(widget = forms.TextInput())
	password	= forms.CharField(widget = forms.PasswordInput(render_value=False))

class RecoveryForm(forms.Form):
	Email = forms.EmailField(error_messages={'invalid': 'Correo invalido'})
	

	def clean(self):
		email = self.cleaned_data.get('Email')

		if not email:
			raise forms.ValidationError("Debe ingresar un correo")

		else:
			try:
				user=User.objects.get(email__exact=email)
			except:
				raise forms.ValidationError("Correo electronico no registrado")

		return self.cleaned_data


class AccountForm(forms.Form):
	Password_Antigua		= forms.CharField(widget = forms.PasswordInput(render_value=False), error_messages={'required': 'Debe proporcionar su Contraseña actual'})
	Nueva_Password			= forms.CharField(widget = forms.PasswordInput(render_value=False), error_messages={'required': 'Debe proporcionar su Nueva contraseña'})
	Repetir_Nueva_Password	= forms.CharField(widget = forms.PasswordInput(render_value=False), error_messages={'required': 'Debe Repetir su nueva contraseña'})

	def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(AccountForm, self).__init__(*args, **kwargs)

	def clean(self):
	    password0 = self.cleaned_data.get('Password_Antigua')
	    password1 = self.cleaned_data.get('Nueva_Password')
	    password2 = self.cleaned_data.get('Repetir_Nueva_Password')

	    if password0 and not self.user.check_password(password0):
	    	raise forms.ValidationError("La contraseña actual no es correcta")

	    if password1 and password2:
	    	if password1 != password2:
	        	raise forms.ValidationError("Las contraseñas no coinciden")
	        if len(password1) < 4:
	    		raise forms.ValidationError("La nueva contraseña debe tener un mínimo de 4 caracteres")
		
		return self.cleaned_data

class EmailForm(forms.Form):
	Email = forms.EmailField(error_messages={'invalid': 'Correo invalido'})

	def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(EmailForm, self).__init__(*args, **kwargs)
         Email = forms.EmailField(label=self.user.email)

	def clean(self):
		email = self.cleaned_data.get('Email')

		if not email:
			forms.ValidationError("Debe ingresar un correo")

		return self.cleaned_data