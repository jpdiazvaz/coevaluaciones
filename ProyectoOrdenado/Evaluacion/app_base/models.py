#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
import django.contrib.auth.models as auth


class Profesor(models.Model):
    RUT = models.CharField(
        max_length = 10,
        help_text = u"Sin puntos y con guión (e.g. 11111111-1)")

    nombre = models.CharField(max_length = 100)

    instituto = models.CharField(
        max_length = 50,
        blank      = True)

    user = models.OneToOneField(
        auth.User,
        related_name = '+')

    def __unicode__(self):
        return u"{0} en {1}".format(
            self.nombre,
            self.instituto or "<sin instituto>")

    class Meta:
        verbose_name_plural = u"profesores"


class ProfesorEvaluador(models.Model):
    profesor = models.ForeignKey(Profesor)

    instancia_ramo = models.ForeignKey('InstanciaRamo')

    colaborador = models.BooleanField(help_text = u"si es profesor colaborador")

    def __unicode__(self):
        return u"profesor evaluador {0} ramo {1}".format(
            self.profesor,
            self.instancia_ramo)

    class Meta:
        verbose_name_plural = u"profesores evaluadores"


class Ramo(models.Model):
    sigla = models.CharField(
        max_length = 10,
        help_text  = u"El código del ramo")

    nombre = models.CharField(
        max_length = 100,
        help_text  = u"El nombre completo del ramo")

    instituto = models.CharField(
        max_length = 50,
        blank      = True)

    def __unicode__(self):
        return self.sigla


class InstanciaRamo(models.Model):
    ramo = models.ForeignKey(Ramo)

    agno = models.IntegerField(verbose_name = u"año")

    opciones_semestre = (
        (1, u'1° semestre'),
        (2, u'2° semestre'),)
    semestre = models.IntegerField(
        default = 1,
        choices = opciones_semestre)

    grupo = models.IntegerField(
        blank = True,
        null  = True)

    def __unicode__(self):
        return u"{0} el {1} de {2}{3}".format(
            self.ramo,
            dict(self.opciones_semestre).get(self.semestre, u"? semestre"),
            self.agno,
            (", G" + str(self.grupo)) if self.grupo is not None else "")

    class Meta:
        verbose_name        = u"instancia de ramo"
        verbose_name_plural = u"instancias de ramo"


class Alumno(models.Model):
    RUT = models.CharField(
        max_length = 10,
        help_text = u"Sin puntos y con guión (e.g. 11111111-1)")

    nombre = models.CharField(max_length = 100)

    user = models.OneToOneField(
        auth.User,
        related_name = '+')

    def __unicode__(self):
        return u"alumno {0}".format(self.nombre)


class Inscripcion(models.Model):
    instancia_ramo = models.ForeignKey(InstanciaRamo)

    alumno = models.ForeignKey(Alumno)

    grupo_por_defecto = models.IntegerField(
        blank = True,
        null  = True)

    def __unicode__(self):
        return u"inscripción de {0} en: {1}".format(self.alumno, self.instancia_ramo)

    class Meta:
        verbose_name        = u"inscripción"
        verbose_name_plural = u"inscripciones"


# Este modelo no tiene mucha incidencia sobre la aplicación, pero
# existe por completitud

class Ayudante(models.Model):
    RUT = models.CharField(
        max_length = 10,
        help_text = u"Sin puntos y con guión (e.g. 11111111-1)")

    nombre = models.CharField(max_length = 100)

    user = models.OneToOneField(
        auth.User,
        related_name = '+')

    ramos = models.ManyToManyField(InstanciaRamo)

    def __unicode__(self):
        return u"ayudante {0}".format(self.nombre)
