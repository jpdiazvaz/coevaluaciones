from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name = 'base.html'),
        name = 'inicio'),
    url(r'^formularios/', include('app_evals.formularios.urls')),
    url(r'^evaluaciones/', include('app_evals.evaluaciones.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'evaluaciones.views.logout_view'),
    url(r'^admin/', include(admin.site.urls)),
)
