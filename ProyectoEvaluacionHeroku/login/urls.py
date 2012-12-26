from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
	url(r'^recuperar_pass/$', 'login.views.recuperar_pass'),
	url(r'^profesor_login/$', 'login.views.profesor_login'),
	url(r'^gestionar_cuenta_contrasena/$', 'login.views.gestionar_cuenta_contrasena'),
	url(r'^gestionar_cuenta_correo/$', 'login.views.gestionar_cuenta_correo'),
)