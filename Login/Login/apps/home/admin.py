from django.contrib import admin
from Login.apps.home.models import Alumno, Profesor, Ayudante, Usuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.admin import UserAdmin

class AlumnoInline(admin.StackedInline):
    model = Alumno

#class ProfesorInline(admin.StackedInline):
 #   model = Profesor

#class AyudanteInline(admin.StackedInline):
#    model = Ayudante

class AlumnoAdmin(UserAdmin):
    inlines = (AlumnoInline,)

#class ProfesorAdmin(UserAdmin):
 #   inlines = (ProfesorInline,)

#class AyudanteAdmin(UserAdmin):
  #  inlines = (AyudanteInline,)


admin.site.unregister(User)

admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Ayudante)
admin.site.register(Usuario)
#admin.site.register(Alumno, AlumnoAdmin)
#admin.site.register(Profesor, ProfesorAdmin)
#admin.site.register(Ayudante, AyudanteAdmin)
#admin.site.register(Usuario, UserAdmin)