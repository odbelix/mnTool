#!/usr/bin/env python

# delete.py, script that manages the elimination of information in the database 
# It has the necessary functions to delete each of the existing elements in the database, 
# however also checks whether it is possible to remove or not owing to the Querying the database 
#for determining whether the element exists or is referenced.
# 
# Copyright (C) 28/10/2015 David Alfredo Medina Ortiz  dmedina11@alumnos.utalca.cl
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

#modules used
import sys
import psycopg2

from ModulosDevice.ComunicacionDB import Comunication
from ModulosDevice.Cruds import Query

#function that allows you to delete a device
#serial => It represents the serial device to remove
def DeleteDevice (serial):
	#first verify if it has relations with another device, that is if  in the table exists in connecting with serialp cannot be removed
	query = "select * from conecta where serialp= '%s'" % serial
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete element white serial ", serial, " because has relations whit other device"
	else:
		#We wonder if it exists in the database...
		query = "select * from dispositivo where serial = '%s'" % serial
		if Query.ExistElementInDB(query) == 0:
			print "Delete connection in table conecta"
			#first i have to delete it in the table links ...
			query = "DELETE FROM conecta where serialh = '%s'" % serial
			Query.DeleteDB(query)
			print "Delete device in table device"
			query = "DELETE  FROM dispositivo where serial = '%s'"% serial
			Query.DeleteDB(query)
		else:
			print "Device whit serial input not exists in data base"

#function that allows to delete a campus
#id_campus => id of the campus to delete 
def DeleteCampus(id_campus):

	#first verify if it doesn't have relation with the table buildings, that is, if building is not referenced to campus with these id...
	query = "select * from edificio where id_campus = %d" % id_campus
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete campus whit id ", id_campus, " because has relations whit other elements"
	else:
		#We ask if the campus exists in the database...
		query = "select * from campus where id_campus = %d" % id_campus
		if Query.ExistElementInDB(query) == 0:
			#manage the consultation ...
			print "Delete campus"
			query = "DELETE FROM campus where id_campus = %d" % id_campus
			Query.DeleteDB(query)
		else:
			print "Not exists a campus whit id ", id_campus, " registered in data base"

#function that allows to delete a building
#id_edificio => id of the building to delete
def DeleteEdificio(id_edificio):

	#first we verify if it doesn't have relation with the table rack
	query = "select * from rack where id_edif = %d" % id_edificio
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete delete building whit id ", id_edificio, " because has relations whit other elements"
	else:
		#We evaluate if the building exists in the database...
		query = "select * from edificio where id_edif = %d" % id_edificio
		if Query.ExistElementInDB(query) == 0:
			#manage the query...
			print "Delete building"
			query = "DELETE FROM edificio where id_edif = %d" % id_edificio
			Query.DeleteDB(query)
		else:
			print "Not exists a building whit id ", id_edificio, " registered in data base"

#function that allows to delete a level
#id_nivel => id of the level to delete
def DeleteNivel(id_nivel):

	#first we verify if it doesn't have relation with the table rack
	query = "select * from rack where id_nivel = %d" % id_nivel
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete level with id ", id_nivel, " because has relations whit other elements"
	else:
		#We evaluate if the level exists in the database...
		query = "select * from nivel where id_nivel = %d" % id_nivel
		if Query.ExistElementInDB(query) == 0:
			#manage the query to delete ...
			print "Delete level"
			query = "DELETE FROM nivel where id_nivel = %d" % id_nivel
			Query.DeleteDB(query)
		else:
			print "Not exists a level whit id ", id_nivel, " registered in data base"

#function that allows to delete a device
#id_tipo_disp => id of the kind of device to delete 
def DeleteTipoDispositivo(id_tipo_disp):

	#first verify if it doesn't have relation with the table modelo
	query = "select * from modelo where id_tipo_disp = %d" % id_tipo_disp
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete model whit id ", id_tipo_disp, " because has relations whit other elements"
	else:
		#we evaluate whether the device type in the database
		query = "select * from tipo_disp where id_tipo_disp = %d" % id_tipo_disp
		if Query.ExistElementInDB(query) == 0:
			#manage the query to delete ...
			print "Delete kind of device"
			query = "DELETE FROM tipo_disp where id_tipo_disp = %d" % id_tipo_disp
			Query.DeleteDB(query)
		else:
			print "Not exists a kind device whit id ", id_tipo_disp, " registered in data base"

#function that allows to delete a model...
#id_modelo => id of the model to delete
def DeleteModelo(id_modelo):

	#first check if it has no relations with the table device
	query = "select * from dispositivo where id_modelo = %d" % id_modelo
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete model with id ", id_modelo, " because has relations whit other elements"
	else:
		#we evaluated whether the model exists in the database
		query = "select * from modelo where id_modelo = %d" % id_modelo
		if Query.ExistElementInDB(query) == 0:
			#manage the query to delete 
			print "Delete model"
			query = "DELETE FROM modelo where id_modelo = %d" % id_modelo
			Query.DeleteDB(query)
		else:
			print "Not exists model whit id ", id_modelo, " registered in data base"

#function that allows to delete a brand...
#id_marca => id of the brand to delete
def DeleteMarca(id_marca):

	#first verify if it has no relations with the table modelo...
	query = "select * from modelo where id_marca = %d" % id_marca
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete marker whit id ", id_marca, " because has relations whit others elements"
	else:
		#we evaluated whether the brand exists in the database
		query = "select * from marca where id_marca = %d" % id_marca
		if Query.ExistElementInDB(query) == 0:
			#manage the query to delete....
			print "Delete marker"
			query = "DELETE FROM marca where id_marca = %d" % id_marca
			Query.DeleteDB(query)
		else:
			print "Not exists marker whit id ", id_marca, " registered in data base"

#function that allows to delete a rack
#id_rack => id dof the rank to delete
def DeleteRack(id_rack):

	#first verify if it has no relations with the table device
	query = "select * from dispositivo where id_rack = %d" % id_rack
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete rack whit id ", id_rack, " because has relations whit others elements"
	else:
		#We evaluate whether the rack exists in the database...
		query = "select * from rack where id_rack = %d" % id_rack
		if Query.ExistElementInDB(query) == 0:
			#manage the query to delete....
			print "Delete rack"
			query = "DELETE FROM  rack where id_rack = %d" % id_rack
			Query.DeleteDB(query)
		else:
			print "Not exists rack white id ", id_rack , " registered in data base"

#function that allowsto delete a kind of link
#id_tipo_enlace => id of the kind of link to delete
def DeleteTipoEnlace(id_tipo_enlace):

	#first verify if it has no relations with the table conecta
	query = "select * from conecta where id_tipo_enlace = %d" % id_tipo_enlace
	if Query.ExistElementInDB(query) == 0:
		print "Is not possible delete kind link whit id ", id_tipo_enlace, " because has relations whit others elements"
	else:
		#We evaluate whether the link type exists in the database...
		query = "select * from tipo_enlace where id_tipo_enlace = %d" % id_tipo_enlace
		if Query.ExistElementInDB(query) == 0:
			#manage the query to delete....
			print "Delete kind of link"
			query = "DELETE FROM  tipo_enlace where id_tipo_enlace = %d" % id_tipo_enlace
			Query.DeleteDB(query)
		else:
			print "Not exists kind of link whit id ", id_tipo_enlace , " registered in data base"	