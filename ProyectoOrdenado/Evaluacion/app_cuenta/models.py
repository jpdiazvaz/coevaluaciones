#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models, transaction
import app_base.models as base

class Formulario(models.Model):
    autor = models.ForeignKey(base.Profesor)

    derivado = models.ForeignKey(
        'self',
        blank     = True,
        null      = True,
        default   = None,
        editable  = False,
        on_delete = models.SET_NULL)

    descripcion = models.TextField(
        verbose_name = u"descripción",
        blank        = True)

    instanciado = models.BooleanField(
        default   = False,
        editable  = False,
        help_text = u"Si ha sido usado como plantilla")

    fecha_creacion = models.DateTimeField(
        auto_now_add = True,
        verbose_name = u"fecha de creación",
        editable     = False)

    ecoevaluacion = models.BooleanField(
        default      = False,
        verbose_name = u"ecoevaluación",
        help_text    = u"Si es eco-evaluación o no")

    numero_hijos = models.PositiveIntegerField(
        default      = 0,
        editable     = False,
        verbose_name = u"número de hijos",
        help_text    = u"El número de formularios que lo han duplicado")

    publicado = models.BooleanField(
        default   = False,
        help_text = u"Si ha sido publicado o no")

    KEYWORDS = models.TextField(blank = True)

    METADATA = models.TextField(blank = True)

    categoria = models.PositiveIntegerField(
        default      = 0,
        editable     = False,
        verbose_name = u"categoría",
        help_text    = u"Cuantas veces ha sido usado en una encuesta.")

    def __unicode__(self):
        return self.descripcion

    def publicar(self):
        """Hace que un formulario esté publicado. Incluye
        actualización en base de datos."""
        if self.descripcion or self.descripcion != '':
            self.publicado = True
            self.save()
        else:
            raise Exception("No es posible publicar un formulario sin descripción.")

    def copiar(self, autor, *fields):
        """Retorna una copia de este formulario.

        La copia será grabada en base de datos. Los campos copiados
        son *fields*, y el resto queda con valores por defecto. El
        campo autor es una excepción y se obtiene del argumento
        requerido *autor*. Además, se copian todas las preguntas y
        opciones asociadas al formulario."""
        f = Formulario()
        with transaction.commit_on_success():
            for field in fields:
                setattr(f, field, getattr(self, field))
            f.autor = autor
            f.save()
            for p in self.pregunta_set.all():
                old_pk = p.pk
                p.pk = None
                p.formulario = f
                p.save()
                for op in Opcion.objects.filter(pregunta__pk = old_pk):
                    op.pk = None
                    op.pregunta = p
                    op.save()
        return f

    class Meta:
        ordering = ['-categoria', '-fecha_creacion']


class Pregunta(models.Model):
    formulario = models.ForeignKey(Formulario)

    orden_p = models.PositiveIntegerField(
        verbose_name = u"orden de pregunta",
        help_text    = u"Posición de la pregunta en la lista de preguntas")

    texto = models.TextField()

    opciones_tipo = (
        ('A', u'alternativas'),
        ('T', u'texto libre'),
        ('N', u'numérica o calificación'),
        ('M', u'selección múltiple'),)
    tipo = models.CharField(
        default    = 'A',
        max_length = 1,
        choices    = opciones_tipo)

    valor_max = models.FloatField(
        blank        = True,
        null         = True,
        verbose_name = u"valor máximo",
        help_text    = u"Máximo valor para una pregunta de tipo numérica")

    valor_min = models.FloatField(
        blank        = True,
        null         = True,
        verbose_name = u"valor mínimo",
        help_text    = u"Mínimo valor para una pregunta de tipo numérica")

    ponderacion = models.FloatField(
        verbose_name = u"ponderación",
        help_text    = u"Ponderación de la pregunta")

    opciones_formato = (
        ('R', u'real'),
        ('E', u'entero'),)
    formato = models.CharField(
        blank      = True,
        null       = True,
        max_length = 1,
        choices    = opciones_formato,
        help_text  = u"Si las respuestas de tipo numérico "
                     u"son reales o enteros")

    def __unicode__(self):
        return u"pregunta id {0} de formulario id {1}".format(self.pk,
                                                              self.formulario.pk)

    class Meta:
        ordering = ['formulario', 'orden_p']


class FormularioEvaluacion(models.Model):
    formulario = models.ForeignKey(Formulario)

    evaluacion = models.ForeignKey('Evaluacion')

    opciones_tipo = (
        ('A', u'auto-evaluación'),
        ('C', u'co-evaluación'),
        ('E', u'eco-evaluación'),
        ('H', u'hetero-evaluación'),)
    tipo = models.CharField(
        default    = 'A',
        max_length = 1,
        choices    = opciones_tipo)

    def __unicode__(self):
        return u"formulario_evaluacion id {0}".format(self.pk)

    class Meta:
        verbose_name        = u"formulario-evaluación"
        verbose_name_plural = u"formulario-evaluaciones"


class Evaluacion(models.Model):
    descripcion = models.TextField(verbose_name = u"descripción")

    activa = models.BooleanField()

    fecha_lanzamiento = models.DateTimeField(
        verbose_name = u"fecha de lanzamiento")

    fecha_finalizacion = models.DateTimeField(
        verbose_name = u"fecha de finalización")

    fecha_recordatorio = models.DateTimeField(
        blank        = True,
        null         = True,
        verbose_name = u"fecha de recordatorio")

    formulario = models.ManyToManyField(
        Formulario,
        through = FormularioEvaluacion)

    profesor_evaluador = models.ForeignKey(
        base.ProfesorEvaluador,
        blank     = True,
        null      = True,
        on_delete = models.SET_NULL)

    instancias_ramo = models.ManyToManyField(
        base.InstanciaRamo,
        through = 'RamoEv')

    def __unicode__(self):
        return u"evaluación id {0} lanzada el {1}".format(
            self.pk,
            self.fecha_lanzamiento)

    class Meta:
        verbose_name        = u"evaluación"
        verbose_name_plural = u"evaluaciones"


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta)

    rubrica = models.TextField(verbose_name = u"rúbrica")

    puntaje = models.FloatField()

    def __unicode__(self):
        return u"opción id {0} de pregunta id {1}".format(self.pk, self.pregunta.pk)

    class Meta:
        verbose_name        = u"opción"
        verbose_name_plural = u"opciones"
        ordering            = ['id']


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta)

    opcion = models.ForeignKey(
        Opcion,
        blank     = True,
        null      = True,
        on_delete = models.SET_NULL)

    persona_ev_emisor = models.ForeignKey(
        'PersonaEv',
        related_name = 'respuestas_emitidas')

    persona_ev_receptor = models.ForeignKey(
        'PersonaEv',
        related_name = 'respuestas_recibidas')

    texto = models.TextField(
        blank = True,
        null  = True)

    def __unicode__(self):
        return u"respuesta id {0} a pregunta id {1}".format(self.pk, self.pregunta.pk)


class RamoEv(models.Model):
    instancia_ramo = models.ForeignKey(base.InstanciaRamo)

    evaluacion = models.ForeignKey(Evaluacion)

    def __unicode__(self):
        return u"ramo_evaluación id {0}".format(self.pk)


class PersonaEv(models.Model):
    ramo_ev = models.ForeignKey(RamoEv)

    inscripcion = models.ForeignKey(
        base.Inscripcion,
        blank     = True,
        null      = True,
        on_delete = models.SET_NULL)

    num_ev = models.CharField(
        max_length   = 45,
        blank        = True,
        null         = True,
        verbose_name = u"número de evaluación",
        help_text    = u"No tengo idea que es esto")

    profesor_responsable = models.ForeignKey(
        base.ProfesorEvaluador,
        blank     = True,
        null      = True,
        on_delete = models.SET_NULL)

    grupo = models.IntegerField()

    def __unicode__(self):
        return u"persona_evaluación id {0}".format(self.pk)
