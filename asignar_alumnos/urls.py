from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'^obtener_alumnos/$', 'asignar_alumnos.views.obtener_alumnos'),
	url(r'^$', 'asignar_alumnos.views.asignar_alumnos'),
)

