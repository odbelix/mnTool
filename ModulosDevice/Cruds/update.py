#!/usr/bin/env python

# update.py, script that allow manage the update at data base of all elements exists in it,
# in base a param script ask the elements that wish set of a particular table making the data
# request by standar input.
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

#Modules use
import sys
import psycopg2

from ModulosDevice.ComunicacionDB import Comunication
from ModulosDevice.Cruds import Query

#validate if is possible cast input to int, return o element cast to int, in other case exit program
def ValidateInput(input_element):

	try:
		return int(input_element)
	except:
		print "You must input int type element"
		sys.exit(1)
	
#function that update device
#serial => serial of device to update
def UpdateDevice(serial):

	print "Update ID Model?\n<1>Yes\n<x>No"#ask if wish update id model of device
	if raw_input() == '1':
		print "Input new ID model"
		id_modelo = raw_input()#get new id model by standard input
		id_modelo = ValidateInput(id_modelo)
		#evaluate if id model input exist in data base and generate the query
		query = "select * from modelo where id_modelo = %d"% id_modelo
		if Query.ExistElementInDB(query) == 0:
			#generate query for update element
			query = "UPDATE dispositivo SET id_modelo = %d where serial = '%s'" % (id_modelo, serial)
			Query.UpdateDB(query)
		else:
			print "ID model is not registered in data base"
	else:
		print "Not changes in id model of device"
	#update name of device
	print "Update name of device?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of device"
		name = raw_input()
		#create tue query
		query = "UPDATE dispositivo SET nom_disp = '%s' where serial = '%s'" % (name, serial)
		Query.UpdateDB(query)
	else:
		print "Not changes in name of device"
	#update observation device
	print "Update observation of device?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new observation"
		observation = raw_input()
		#manage the query
		query = "UPDATE dispositivo SET obs_disp = '%s' where serial = '%s'" % (observation, serial)
		Query.UpdateDB(query)
	else:
		print "Not changes in observation of device"
	#update ip of device
	print "Update IP of device?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new IP of device"
		ip = raw_input()
		#manage query
		query = "UPDATE dispositivo SET ip_disp = '%s' where serial = '%s'" % (ip, serial)
		Query.UpdateDB(query)
	else:
		print "Not changes in IP of device"	
	print "Update ID Rack?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new ID rack"
		id_rack = raw_input()
		id_rack = ValidateInput(id_rack)
		query = "select * from rack where id_rack = %d"% id_rack
		if Query.ExistElementInDB(query) == 0:
			query = "UPDATE dispositivo SET id_rack = %d where serial = '%s'" % (id_rack, serial)
			Query.UpdateDB(query)
		else:
			print "ID rack is not registered in data base"
	else:
		print "Not changes in ID rack of device"
	print "Update number of door device?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input number of doors of device"
		num_puertas = raw_input()
		num_puertas = ValidateInput(num_puertas)
		query = "UPDATE dispositivo SET ptas_disp = %d where serial = '%s'" % (num_puertas, serial)
		Query.UpdateDB(query)
	else:
		print "Not changes in number doors of device"

#Update campus
#id_campus => id of campus to update
def UpdateCampus(id_campus):

	id_campus = int(id_campus)#set to int
	print "Update name of Campus?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of campus"
		name_campus = raw_input()
		#gestionamos la consulta para modificar el nombre de campus...
		query = "UPDATE campus SET nom_campus = '%s' where id_campus = %d"% (name_campus, id_campus)
		Query.UpdateDB(query)
	else:
		print "Not changes in name of campus"

#Update level
#id_nivel => id of level to update
def UpdateNivel(id_level):

	id_level = int(id_level)
	print "Update name of level\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of level"
		name_level = raw_input()
		query = "UPDATE nivel SET nom_nivel = '%s' where id_nivel = %d"% (name_level, id_level)
		Query.UpdateDB(query)
	else:
		print "Not changes in name of level"

#Update building
#id_building => representa el id del edificio a Update
def UpdateEdificio(id_building):

	id_building = int(id_building)
	print "Update id of campus\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new id of campus"
		id_campus = raw_input()
		id_campus = ValidateInput(id_campus)
		#ask if exist id in data base
		query = "select * from campus where id_campus = %d" % id_campus
		if Query.ExistElementInDB(query) == 0:
			#gestionamos la consulta para modificar el atributo...
			query = "UPDATE edificio SET id_campus = %d where id_edif = %d" % (id_campus, id_building)
			Query.UpdateDB(query)
		else:
			print "ID campus not in data base"
	else:
		print "Not changes in id of campus for building"
	print "Update name of building\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input name of building"
		name_building = raw_input()
		query = "UPDATE edificio set nom_edif = '%s' where id_edif = %d" % (name_building, id_building)
		Query.UpdateDB(query)
	else:
		print "Not changes in name of building"

#Update marker
#id_marker => id of marker to set atributes
def UpdateMarca(id_marker):

	id_marker = int(id_marker)
	print "Update name of marker\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of marker"
		name_marker = raw_input()
		query = "UPDATE marca SET nom_marca = '%s' where id_marca = %d"% (name_marker, id_marker)
		Query.UpdateDB(query)
	else:
		print "Not chanes in name of marker"

#Update model
#id_model => id of model to set atributes
def UpdateModelo(id_model):

	id_model = int(id_model)
	print "Update name of model\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of model"
		name_model = raw_input()
		query = "UPDATE modelo SET nom_modelo = '%s' where id_modelo = %d"% (name_model, id_model)
		Query.UpdateDB(query)
	else:
		print "Not changes in name of model"
	#update id of kind device
	print "Update id of kind device\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input id of kind device"
		id_kind = raw_input()
		id_kind = ValidateInput(id_kind)
		#check if id of kind device exist in data base
		query = "select * from tipo_disp where id_tipo_disp = %d" % id_kind
		if Query.ExistElementInDB(query) == 0:
			query = "UPDATE modelo SET id_tipo_disp = %d where id_modelo = %d" % (id_kind, id_model)
			Query.UpdateDB(query)
		else:
			print "ID kind device not in data base"
	else:
		print "Not changes in id of kind device"
	#update id of marker
	print "Update id of marker\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new  id of marker"
		id_marker = raw_input()
		id_marker = ValidateInput(id_marker)
		query = "select * from marca where id_marca = %d" % id_marker
		if Query.ExistElementInDB(query) == 0:
			query = "UPDATE modelo SET id_marca = %d where id_modelo = %d" % (id_marker, id_model)
			Query.UpdateDB(query)
		else:
			print "ID of marker not in data base"
	else:
		print "Not changes in id of marker"

#Update rack
#id_rack => represente id of rack to update
def UpdateRack(id_rack):

	id_rack = int(id_rack)
	print "Update detail of rack?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new detail"
		detalle = raw_input()
		query = "UPDATE rack SET detalle = '%s' where id_rack = %d"% (detalle, id_rack)
		Query.UpdateDB(query)
	else:
		print "Not changes in atribute detail"
	#update id of level
	print "Update id of level?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new id of level"
		id_nivel = raw_input()
		id_nivel = ValidateInput(id_nivel)
		query = "select * from nivel where id_nivel = %d" % id_nivel
		if Query.ExistElementInDB(query) == 0:
			query = "UPDATE rack SET id_nivel = %d where id_rack = %d" % (id_nivel, id_rack)
			Query.UpdateDB(query)
		else:
			print "ID level not exists in data base"
	else:
		print "Not changes in atribute id_nivel"
	#update id of building
	print "Update id of building?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new id of building"
		id_building = raw_input()
		id_building = ValidateInput(id_building)
		query = "select * from edificio where id_edif = %d" % id_building
		if Query.ExistElementInDB(query) == 0:
			query = "UPDATE rack SET id_edif = %d where id_rack = %d" % (id_building, id_rack)
			Query.UpdateDB(query)
		else:
			print "ID of building not exists in data base"
	else:
		print "Not changes in atribute id_edif"

#Update kind link
#id_enlace is a element to update in data base
def UpdateEnlace(id_enlace):

	id_enlace = int(id_enlace)
	print "Update name of kind link?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of kind link"
		nombre = raw_input()
		query = "UPDATE tipo_enlace SET nom_tipo_enlace = '%s' where id_marca = %d"% (nombre, id_enlace)
		Query.UpdateDB(query)
	else:
		print "Not changes in atribute nom_marca"

#Update kind device
#id_kind is a element to update in data base
def UpdateKindDevice(id_kind):

	id_kind = int(id_kind)
	print "Update name of kind device?\n<1>Yes\n<x>No"
	if raw_input() == '1':
		print "Input new name of kind device"
		nombre = raw_input()
		query = "UPDATE tipo_disp SET nom_tipo_disp = '%s' where id_tipo_disp = %d"% (nombre, id_kind)
		Query.UpdateDB(query)
	else:
		print "Not changes in atribute nom_tipo_disp"