from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('Login.apps.home.views',
	#url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^ingresar/$', 'index_view', name='vista_principal'),
	url(r'^logout/$', 'logout_view', name='vista_logout'),
	url(r'^profesor_login/$', 'profesor_view', name='vista_profesor'),
	url(r'^recuperar_pass/$', 'recover_view', name='vista_recuperar'),
	url(r'^gestionar_cuenta/$', 'account_view', name='vista_account'),
	url(r'^ver_asignaturas/$', 'subjects_view', name='vista_subjects'),
	url(r'^asignatura1/$', 'subject1_view', name='vista_subject1'),
	url(r'^evaluation1/$', 'evaluation1_view', name='vista_evaluation1'),
	url(r'^distribution1/$', 'distribution1_view', name='vista_distribution1'),
	url(r'^add_student1/$', 'add_student1_view', name='vista_agregar_alumno1'),
	url(r'^properties/$', 'properties_view', name='vista_propiedades'),
	)