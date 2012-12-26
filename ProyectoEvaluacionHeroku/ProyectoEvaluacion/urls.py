from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
	url(r'^profesor_login/$', 'login.views.profesor_login'),
	url(r'^recuperar_pass/$', 'login.views.recuperar_pass'),
	url(r'^gestionar_cuenta_contrasena/$', 'login.views.gestionar_cuenta_contrasena'),
	url(r'^gestionar_cuenta_correo/$', 'login.views.gestionar_cuenta_correo'),
	url(r'^asignar_alumnos/$', include('asignar_alumnos.urls')),
	url(r'^asignar_alumnos/obtener_alumnos/$', 'asignar_alumnos.views.obtener_alumnos'),
	url(r'^asignar_alumnos/cargar_distribucion/$', 'asignar_alumnos.views.cargar_distribucion'),
	url(r'^asignar_alumnos/solicitar_distribuciones/$', 'asignar_alumnos.views.distribuciones_disponibles'),
	url(r'^logout/$', 'ProyectoEvaluacion.views.logout_vista'),
    url(r'^admin/', include(admin.site.urls)),
)
