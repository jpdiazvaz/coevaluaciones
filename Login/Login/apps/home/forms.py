from django import forms

class LoginForm(forms.Form):
	username	= forms.CharField(widget = forms.TextInput())
	password	= forms.CharField(widget = forms.PasswordInput(render_value=False))

class RecoveryForm(forms.Form):
	Email	= forms.CharField(widget = forms.TextInput())

