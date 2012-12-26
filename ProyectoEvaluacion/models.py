from django.db import models
from django.contrib.auth.models import User


class Alumno(models.Model):
    user = models.OneToOneField(User)
    rut = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=300)
    class Meta:
        db_table = u'alumno'    
    def __unicode__(self):
        return u"rut: {0}; nombre: {1}".format(self.rut, self.nombre)


class Ramo(models.Model):
    id_ramo = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=300)
    instituto = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'ramo'

class InstanciaRamo(models.Model):
    id_instancia_ramo = models.IntegerField(primary_key=True)
    id_ramo = models.ForeignKey(Ramo, db_column='id_ramo')
    ango = models.IntegerField()
    semestre = models.BooleanField(default=False) 
    grupo = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'instancia_ramo'


class Inscripcion(models.Model):
    id_instancia_ramo = models.ForeignKey(InstanciaRamo, db_column='id_instancia_ramo')
    grupo_por_defecto = models.IntegerField(null=True, blank=True)
    id_alumno = models.ForeignKey(Alumno,db_column='id_alumno')
    class Meta:
        db_table = u'inscripcion'


class Ayudante(models.Model):        
    user = models.OneToOneField(User)
    rut = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=300)
    class Meta:
        db_table = u'ayudante'


class AyudanteRamo(models.Model):
    id_instancia_ramo = models.ForeignKey(InstanciaRamo, primary_key=True, db_column='id_instancia_ramo')    
    id_ayudante = models.ForeignKey(Ayudante, db_column='id_ayudante')
    class Meta:
        db_table = u'ayudante_ramo'


class Profesor(models.Model):
    user = models.OneToOneField(User)
    rut = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=300)
    instituto = models.CharField(max_length=135, blank=True)    
    class Meta:
        db_table = u'profesor'


class Formulario(models.Model):
    id_formulario = models.IntegerField(primary_key=True)
    id_profesorautor = models.ForeignKey(Profesor, db_column='id_profesorAutor')
    derivado = models.ForeignKey('self', db_column='derivado')
    autor = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=600)
    instanciado = models.BooleanField(default=False) 
    fecha_creacion = models.DateField()
    ecoevaluacion = models.BooleanField(default=False) 
    numero_hijos = models.IntegerField()
    publicado = models.BooleanField(default=False)
    metadata = models.TextField(db_column='METADATA')
    categoria = models.IntegerField()
    class Meta:
        db_table = u'formulario'


class Pregunta(models.Model):
    id_pregunta = models.IntegerField(primary_key=True)
    id_formulario = models.ForeignKey(Formulario, db_column='id_formulario')
    orden_p = models.IntegerField()
    texto = models.CharField(max_length=1500)
    tipo = models.CharField(max_length=21)
    valor_max = models.FloatField(null=True, blank=True)
    valor_min = models.FloatField(null=True, blank=True)
    ponderacion = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'pregunta'


class Opcion(models.Model):
    id_opcion = models.IntegerField(primary_key=True)
    id_pregunta = models.ForeignKey(Pregunta, db_column='id_pregunta')
    rubrica = models.CharField(max_length=3000)
    puntaje = models.FloatField()
    class Meta:
        db_table = u'opcion'


class ProfesorResponsable(models.Model):
    id_profesor_responsable = models.IntegerField(primary_key=True)
    id_instancia_ramo = models.ForeignKey(InstanciaRamo, db_column='id_instancia_ramo')
    id_profesor = models.ForeignKey(Profesor, db_column='id_profesor')
    colaborador = models.BooleanField()
    class Meta:
        db_table = u'profesor_responsable'


class Evaluacion(models.Model):
    id_evaluacion = models.IntegerField(primary_key=True)
    id_profesor = models.ForeignKey(Profesor, db_column='id_profesor')
    descripcion = models.CharField(max_length=3000)
    activa = models.BooleanField(default=False)
    fecha_lanzamiento = models.DateField()
    fecha_finalizacion = models.DateField()
    fecha_recordatorio = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'evaluacion'


class RamoCoev(models.Model):
    id_instancia_ramo = models.ForeignKey(InstanciaRamo, primary_key=True, db_column='id_instancia_ramo')
    id_coevaluacion = models.ForeignKey(Evaluacion, db_column='id_coevaluacion')
    class Meta:
        db_table = u'ramo_coev'



class PersonaCoev(models.Model):
    id_persona_coev = models.IntegerField(primary_key=True)
    id_instancia_ramo = models.ForeignKey(Inscripcion, db_column='id_instancia_ramo',related_name="PersonaCoev_instancia_ramo+") #Se agrego un related_name
    id_coevaluacion = models.ForeignKey(RamoCoev, db_column='id_coevaluacion')
    id_alumno = models.ForeignKey(Inscripcion, null=True, db_column='id_alumno', blank=True,related_name="PersonaCoev_id_alumno+") #Se agrego un related_name
    num_coev = models.CharField(max_length=135, blank=True)
    id_profesor_responsable = models.ForeignKey(ProfesorResponsable, null=True, db_column='id_profesor_responsable', blank=True)
    grupo = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'persona_coev'


class Respuesta(models.Model):
    id_respuesta = models.IntegerField(primary_key=True)
    id_pregunta = models.ForeignKey(Pregunta, db_column='id_pregunta')
    id_opcion = models.ForeignKey(Opcion, null=True, db_column='id_opcion', blank=True)
    id_persona_coev_emisor = models.ForeignKey(PersonaCoev, db_column='id_persona_coev_emisor',related_name="respuesta_emisor+") #Se agrego un related_name
    id_persona_coev_receptor = models.ForeignKey(PersonaCoev, db_column='id_persona_coev_receptor',related_name="respuesta_receptor+") #Se agrego un related_name
    texto = models.TextField(blank=True)
    valor = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'respuesta'


class FormularioEvaluacion(models.Model):
    id_formulario = models.ForeignKey(Formulario, db_column='id_formulario')
    id_evaluacion = models.ForeignKey(Evaluacion, db_column='id_evaluacion')
    tipo = models.CharField(max_length=21, primary_key=True)
    class Meta:
        db_table = u'formulario_evaluacion'