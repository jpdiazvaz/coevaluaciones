from django import forms

class LoginForm(forms.Form):
	username	= forms.CharField(widget = forms.TextInput())
	password	= forms.CharField(widget = forms.PasswordInput(render_value=False))

class RecoveryForm(forms.Form):
	Email	= forms.CharField(widget = forms.TextInput())

class AccountForm(forms.Form):
	Correo_Electronico		= forms.CharField(widget = forms.TextInput())	
	Password_Antigua		= forms.CharField(widget = forms.PasswordInput(render_value=False))
	Nueva_Password			= forms.CharField(widget = forms.PasswordInput(render_value=False))
	Repetir_Nueva_Password	= forms.CharField(widget = forms.PasswordInput(render_value=False))