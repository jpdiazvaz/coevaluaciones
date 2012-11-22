#!/usr/bin/python
# -*- coding: utf-8 -*-
""" invocación en Linux: ./nombre_de_este_archivo <archivo con mail, pass y primer_nombre, separados por espacios> """
import sys
import csv
import smtplib
import subprocess

# retorna conteo de lineas de un archivo
def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

# cuenta lineas del archivo
num_al = file_len(sys.argv[1])

#abre archivo
ip = csv.reader(open(sys.argv[1], "rb"), delimiter=" ")

# conecta con servidor de correo (sólo lo he probado con correos basados en gmail)
print "conectando con servidor de correo..."
username = 'drigox90rih@gmail.com'
password = ''
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)

print "enviando correos..."
for i in range(num_al):
	line = ip.next()
	mail = line[0]
	passw = line[1]
	nombre = line[2]
	print"------------------------- Enviando a: "+nombre
	# compone mensaje
	msg = "Subject: Extensión plazo de coevaluación\r\nEstimado(a) "+nombre+",\n\nEn caso que aún no hayas respondido la encuesta en el sitio http://www.inf.uach.cl/maturana/Coeval2/ , te informo que el plazo para hacerlo se ha extendido hasta las 23h59 del lunes 2 de julio.\n Recuerda que tu password es "+passw+" y que si no respondes tendrás un 1.0 en el ítem de coevaluación.\n\nCordialmente,\n\nJorge Maturana\nhttp://www.inf.uach.cl/maturana   +56 63 22 1817"
	# compone lista de destinatarios
	toaddrs = list()
	toaddrs.append(mail)
	#print msg
	#print toaddrs
	#envía el correo
	server.sendmail(username, toaddrs, msg)
	
#cierra la conexión con el servidor de correo
server.quit()

