#!/usr/bin/env python

# MakeTreeFull.py, script que permite generar un arbol completo con respecto a la informacion que 
# existe en la base de datos.
# 
# Copyright (C) 14/10/2015 David Alfredo Medina Ortiz  dmedina11@alumnos.utalca.cl
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

#Modulos a utilizar
import sys
import psycopg2

from ModulosDevice.ComunicacionDB import Comunication
from ModulosDevice.Cruds import Query
from ModulosDevice.GenerationTree import MakeTreeDispositivos

def MakeTree ():

	#establecemos la comunicacion
	database = Comunication.BeginComunication()

	#obtenemos en una lista aparte la informacion de los niveles...
	query = "SELECT * FROM nivel"
	niveles = Comunication.MakeQueryDB (query, database[1])#gestionamos la consulta

	#creamos una consulta...
	query = "SELECT * FROM campus"

	info_campus = Comunication.MakeQueryDB (query, database[1])#gestionamos la consulta

	for element in info_campus:

		#No mostrare los campus si no tienen edificios...
		#se obtiene la informacion de los edificios...
		query = "SELECT * FROM edificio where id_campus = %d" % element[0]

		if Query.ExistElementInDB(query) == 0:
			info_edificios = Comunication.MakeQueryDB(query, database[1])#gestionamos la consulta
			print "├─Campus: %s" %element[1]
			for edificios in info_edificios:

				#no mostrare los edificios si no tiene racks asociados
				query = "select * from edificio join rack on (edificio.id_edif = rack.id_edif) where edificio.id_edif=%d" % int(edificios[0])
				if Query.ExistElementInDB(query) == 0:
					print "│    ├─Edificio: '%s'" % edificios[2]
					#por cada nivel del edificio obtenemos los rack...
					for nivel in niveles:
						query = "select * from rack join edificio on (rack.id_edif = edificio.id_edif) join nivel on (nivel.id_nivel = rack.id_nivel) where rack.id_nivel = %d AND rack.id_edif = %d" % (nivel[0], edificios[0])
						#evaluamos si el edificio tiene los niveles indicados...
						if Query.ExistElementInDB(query) == 0:
							racks_niveles = Comunication.MakeQueryDB(query, database[1])
							print "│    │    ├─Nivel : ", nivel[1]
							for rack in racks_niveles:#informacion de los rack
								print "│    │    │    ├─Rack: ", rack[3]
								#por cada rack obtenemos la informacion de los dispositivos existentes en el...
								query = "select dispositivo.serial, dispositivo.nom_disp, dispositivo.ip_disp, modelo.nom_modelo, tipo_disp.nom_tipo_disp, marca.nom_marca from dispositivo join rack on (rack.id_rack = dispositivo.id_rack) join modelo on (dispositivo.id_modelo = modelo.id_modelo) join tipo_disp on (tipo_disp.id_tipo_disp = modelo.id_tipo_disp) join marca on (marca.id_marca = modelo.id_marca) where dispositivo.id_rack= %d" %rack[0]
								dispositivo_rack = Comunication.MakeQueryDB(query, database[1])
								#evaluamos aquellos que son papas y con ellos formamos el arbol
								dispositivo_rack_papa = []
								for dispositivo in dispositivo_rack:
									if Query.IsPapa(dispositivo[0]) == 1:
										dispositivo_rack_papa.append(dispositivo[0])
								#ahora hacemos el arbol en base a la lista obtenida...
								#creamos una lista con los elementos que ya han sido buscados...
								list_elements_shows = []
								#recorremos la lista de seriales que son papas...	
								for element in dispositivo_rack_papa:
									#evaluamos si ya mostramos a el y sus hijos...
									if MakeTreeDispositivos.ExisteInLista(list_elements_shows, element) == 0:
										list_parcial = Query.CreateTreeBySerial(element, list_elements_shows, '│    │    │    │    ')#creamos el arbol para ese dispositivo...
										#agregamos los elementos a la lista de elementos mostrados...
										Query.AddElement(list_parcial, list_elements_shows)
	return 0
