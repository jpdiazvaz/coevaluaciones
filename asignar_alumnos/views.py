from django.shortcuts import render_to_response,render
from ProyectoEvaluacion.models import Ramo,Alumno,Profesor,Evaluacion
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
from django.http import HttpResponse
from django.db import connection, transaction
import json
import datetime

def asignar_alumnos(request):
	user = request.user
	ramos = Ramo.objects.raw('SELECT ramo.id_ramo, ramo.nombre FROM ramo,instancia_ramo,profesor_responsable,profesor WHERE ramo.id_ramo = instancia_ramo.id_ramo AND  instancia_ramo.id_instancia_ramo = profesor_responsable.id_instancia_ramo AND  profesor_responsable.id_profesor = profesor.id AND profesor.rut = %s GROUP BY ramo.id_ramo',(user.username))
	return render(request, 'asignar_alumnos.html',locals()) 

def obtener_alumnos(request):
	ramo = request.GET.get('id')
	mostrar = request.GET.get('checked')

	alumnos = Alumno.objects.raw('SELECT alumno.id, alumno.rut, alumno.nombre FROM alumno,instancia_ramo,inscripcion,ramo WHERE alumno.id = inscripcion.id_alumno AND inscripcion.id_instancia_ramo = instancia_ramo.id_instancia_ramo AND instancia_ramo.id_ramo = ramo.id_ramo AND ramo.sigla = %s',(ramo))
	
	datos = []
	datos.append(ramo);
	datos.append(mostrar);
	for a in alumnos:
		datos.append(a.rut)
		datos.append(a.nombre)
	return HttpResponse(json.dumps(datos),content_type='application/json')

def cargar_distribucion(request):
	distribucion = request.GET.get('distribucion')
	if (not distribucion):
		return;

	query = """SELECT persona_coev.grupo, alumno.rut FROM persona_coev, alumno,inscripcion,ramo_coev,evaluacion,instancia_ramo WHERE alumno.id = inscripcion.id_alumno AND inscripcion.id_instancia_ramo = instancia_ramo.id_instancia_ramo AND instancia_ramo.id_instancia_ramo = ramo_coev.id_instancia_ramo AND inscripcion.id_alumno = persona_coev.id_alumno AND persona_coev.id_coevaluacion = ramo_coev.id_coevaluacion AND ramo_coev.id_coevaluacion = evaluacion.id_evaluacion """
	query += "AND evaluacion.id_evaluacion = " + distribucion +";"

	print(query)

	cursor = connection.cursor()
	cursor.execute(query);
	datos = []
	distribucion = cursor.fetchall()
	for dist in distribucion:
		datos.append(dist[1])
		datos.append(dist[0])

	return HttpResponse(json.dumps(datos),content_type='application/json')



def encode_datetime(obj):
	return obj.astimezone(tz.tzutc()).strftime('%Y-%m-%dT%H:%M:%SZ')


def distribuciones_disponibles(request):
	user = request.user
	id_profe = Profesor.objects.raw('SELECT profesor.id FROM profesor WHERE profesor.rut = %s',(user.username))
	sigla_ramos = request.GET.get('ramos')

	""" todas las evaluaciones del profesor """
	query = """SELECT evaluacion.id_evaluacion,evaluacion.descripcion,evaluacion.fecha_lanzamiento FROM ramo_coev,evaluacion,profesor,instancia_ramo,ramo WHERE ramo_coev.id_instancia_ramo = instancia_ramo.id_instancia_ramo AND instancia_ramo.id_ramo = ramo.id_ramo AND ramo_coev.id_coevaluacion = evaluacion.id_evaluacion AND evaluacion.id_profesor = profesor.id"""
	query += " AND profesor.id = " + str(id_profe[0].id)
	query += " AND ("

	sigla_ramos = sigla_ramos[:-1]
	sigla_ramos = sigla_ramos.split(',')
	for i in range(0,len(sigla_ramos)):
		query += " ramo.sigla = '"+sigla_ramos[i]+"' "
		if i != (len(sigla_ramos)-1):
			query += "OR"
		else:
			query += ") "

	query += 'AND('
	for i in range(0,len(sigla_ramos)):
		query += "evaluacion.id_evaluacion NOT IN ("
		query += """SELECT evaluacion.id_evaluacion FROM ramo_coev,evaluacion,profesor,instancia_ramo,ramo WHERE ramo_coev.id_instancia_ramo = instancia_ramo.id_instancia_ramo AND instancia_ramo.id_ramo = ramo.id_ramo AND ramo_coev.id_coevaluacion = evaluacion.id_evaluacion AND evaluacion.id_profesor = profesor.id"""
		query += " AND profesor.id = " + str(id_profe[0].id)
		query += " AND (ramo.sigla != '" + sigla_ramos[i] + "'))"

		if i != (len(sigla_ramos)-1):
			query += " XOR NOT "

	query += ') GROUP BY id_evaluacion;'


	print(query)

	datos = []
	cursor = connection.cursor()
	cursor.execute(query)
	distribucion = cursor.fetchall()

	for dist in distribucion:
		datos.append(dist[0])
		datos.append(dist[1])
		datos.append(str(dist[2]))

	return HttpResponse(json.dumps(datos),content_type='application/json')



