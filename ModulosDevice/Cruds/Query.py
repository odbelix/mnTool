#!/usr/bin/env python

# Query.py, script that allow manage querys to data base of different kind, as well as
# it has required functions for manage of generation of tree based on the information
# given by user
#   
# Copyright (C) 15/10/2015 David Alfredo Medina Ortiz  dmedina11@alumnos.utalca.cl
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

#Modules to use
import sys
import psycopg2
import os

from ModulosDevice.ComunicacionDB import Comunication

#function that show elements whit less format...
def ShowElementsinDataBase(query, title):
	
	#start connection whit data base
	database = Comunication.BeginComunication()
	response = Comunication.MakeQueryDB (query, database[1])#get the response in base of query makye

	#create file for send element in response
	file_response = open("temp", 'w')
	var = "%s\n"%title
	file_response.write(var)
	#shows the results whit format ->
	for element in response:
		file_response.write("->")
		cont=0#for ask if is the first element or no
		for element_in_response in element:
			if cont < len(element)-1:
				var =  "%s;"%element_in_response
				file_response.write(var)
			else:
				file_response.write(element_in_response)
			cont+=1
		file_response.write("\n")

	#close file...
	file_response.close()

	#show file whit less option...
	os.system("less temp")

#function that generate the query at data base received by arguments, printing the results in a format created
#query => is the query for data base thar must be manage
def MakeQuery(query):

	#start connection whit data base
	database = Comunication.BeginComunication()
	response = Comunication.MakeQueryDB (query, database[1])#get the response in base of query makye
	#shows the results whit format ->
	for element in response:
		print "->",
		cont=0#for ask if is the first element or no
		for element_in_response in element:
			if cont < len(element)-1:
				print element_in_response, ";",
			else:
				print element_in_response
			cont+=1
		print 

#function that generate a insert in data base received by arguments.
#query => is the query for insert data in data base 
def InsertDB(query):

	#start connection whit data base
	database = Comunication.BeginComunication()
	try:#error and validation 
		database[1].execute(query)#execute the query
		database[0].commit()#commit the data base whit new information inserted.
		print "Add new element is ok!"
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#function that get the max value of id in table that received by arguments
#table => table in data base to get the max value
#id_table => field of table in data base that will be used as referenced to get the max value
def GetMaxIDinTable(table, id_table):

	#star connection whit data base
	database = Comunication.BeginComunication()
	try:#error and validation
		query = "select MAX(%s) from %s" % (id_table, table);#create query for get max value
		database[1].execute(query)
		for row in database[1]:
			return row[0]#return of max value finded
			break#break of iteration
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)	

#function that allow evaluate if a element exists in data base or not, return 0 if existe or 1 if not exist
#query => is the query of search of information in data base
def ExistElementInDB(query):

	#start conecction whit data base
	database = Comunication.BeginComunication()
	existe =1#value of init search
	try:
		database[1].execute(query)#execute the query
		for row in database[1]:#get values
			existe = 0#set value of indicator
			break#break of iteration
		return existe#return of indicator
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#funtion that allow generate a delete of element in data base
#query => is the query whit information for delete element in data base
def DeleteDB(query):

	#start connection whit data base
	database = Comunication.BeginComunication()
	try:#error and validation
		database[1].execute(query)#execute query
		database[0].commit()#commit the data base
		print "Delete of element is ok!"
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#funtion that allow generate a update of element in data base
#query => is the query whit information for update element in data base
def UpdateDB(query):

	#start connection whit data base
	database = Comunication.BeginComunication()
	try:#error and validation
		database[1].execute(query)#execute query
		database[0].commit()#commit the data base
		print "Update of element is ok!"
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#function that allow return a list whit information of one device according its serial
#serial => serial of device that allow search its information in data base.
def GetInforDeviceBySerial(serial):

	#start connection whit data base
	database = Comunication.BeginComunication()	
	information_device = []#list that will store information of device
	#make the query
	query = "select dispositivo.serial, dispositivo.nom_disp, dispositivo.ip_disp from dispositivo  where dispositivo.serial= '%s'" %serial
	try:#error and validation
		database[1].execute(query)#execute the query
		for row in database[1]:#get results
			for element in row:#get by row of information
				information_device.append(element)#add element in list
			break#break iteration for not make a lot of iteration whitout sense
		return information_device
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)
	
#funtion that allow get the quantity of repeat of ip exist in data base
#query => is the query to generate for data base
def IPisUnica(query):

	cantidad =0#will store the number of repeat ip
	#start connection with data base
	database = Comunication.BeginComunication()	
	try:#error and validation
		database[1].execute(query)#execute the query
		for row in database[1]:
			cantidad = row[0]#get number of repeat
		return cantidad#return number of repeat
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#function that allow get serial of device by its ip address
#query => is the query for data base
def GetSerialbyIP(query):

	#start connection with data base
	database = Comunication.BeginComunication()	
	try:#error and validation
		database[1].execute(query)#execute the query
		for row in database[1]:
			return row[0]#return the serial getting
			break
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#function that allow return a list whit the serials of sons of device by serial
#serial => is the serial for get sons of device
def GetHijosOfDevice(serial):

	#start connection with data base
	database = Comunication.BeginComunication()	
	hijos_device = []#will store of list serials
	#make the query
	query = "select serialh from conecta where serialp = '%s'" % serial
	try:#error and validation
		database[1].execute(query)#execute the query
		for row in database[1]:#get all results
			hijos_device.append(row[0])#add a list
		return hijos_device#erturn list with results query
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#function that receive a serial and evalaute if has son devices
#serial => is a tentative father serial
def IsPapa(serial):
	#start connection whit data base
	database = Comunication.BeginComunication()	
	existe = 0
	query = "select serialp from conecta where serialp = '%s'" % serial
	try:
		database[1].execute(query)#execute the query
		for row in database[1]:
			existe = 1#set value if existe element
			break#break of iteration
		return existe#return value of response query
	except psycopg2.DatabaseError, e:
		print 'Error %s', e
		sys.exit(1)

#function that allow add element of list origin to other list
#list_origen => list with elements to copy
#list_destino => list receive elements
def AddElement(list_origen, list_destino):

	for element in list_origen:
		list_destino.append(element)

#function that evaluate if element exist in list
#element => element to search in list
#lista => list all elements
def ExisteInLista(element, lista):

	existe=0
	for elemento in lista:#get value of list
		if element == elemento:#compare elements
			existe=1#set value
			break#break of iteration
	return existe#return value

#make recursive!!!!!!!
#function that allow create a tree by serial
#serial => serial that generate start of tree
#list_elements => represent the list of all elements already insert tree
def CreateTreeBySerial(serial, list_elements, inicio):

	list_total_dispositivos = []#create list with all elements in tree
	#add serial father device
	list_total_dispositivos.append(serial)
	#get information
	print inicio, "├─", GetInforDeviceBySerial(serial)
	#has son device?
	hijos = GetHijosOfDevice(serial)
	AddElement(hijos, list_total_dispositivos)
	#evaluate len of list
	if len(hijos) >0:
		for hijo in hijos:
			if ExisteInLista(hijo, list_elements)==0:
				print inicio, "│    ├─", GetInforDeviceBySerial(hijo)
				#evaluate if has son device
				segundo_hijos = GetHijosOfDevice(hijo)
				AddElement(segundo_hijos, list_total_dispositivos)
				#evaluate lef of list
				if len (segundo_hijos) >0:
					for seg_hijo in segundo_hijos:
						if ExisteInLista(seg_hijo, list_elements)==0:
							print inicio, "│    │    ├─", GetInforDeviceBySerial(seg_hijo)
							tercer_hijos = GetHijosOfDevice(seg_hijo)
							AddElement(tercer_hijos, list_total_dispositivos)
							if len (tercer_hijos) >0:
								for tercer_hijo in tercer_hijos:
									if ExisteInLista(tercer_hijo, list_elements)==0:
										print inicio, "│    │    │    ├─", GetInforDeviceBySerial(tercer_hijo)
										cuarto_hijos = GetHijosOfDevice(tercer_hijo)
										AddElement(cuarto_hijos, list_total_dispositivos)
										if len (cuarto_hijos) > 0:
											for cuarto_hijo in cuarto_hijos:
												if ExisteInLista(cuarto_hijo, list_elements)==0:
													print inicio, "│    │    │    │    ├─", GetInforDeviceBySerial(cuarto_hijo)
													quinto_hijos = GetHijosOfDevice(cuarto_hijo)
													AddElement(quinto_hijos, list_total_dispositivos)
													if len (quinto_hijos) > 0:
														for quinto_hijo in quinto_hijos:
															if ExisteInLista(quinto_hijo, list_elements)==0:
																print inicio, "│    │    │    │    │    ├─", GetInforDeviceBySerial(quinto_hijo)							
																sexto_hijos = GetHijosOfDevice(quinto_hijo)
																AddElement(sexto_hijos, list_total_dispositivos)
																if len (sexto_hijos) > 0:
																	for sexto_hijo in sexto_hijos:
																		if ExisteInLista(sexto_hijo, list_elements)==0:
																			print inicio, "│    │    │    │    │    │    ├─", GetInforDeviceBySerial(sexto_hijo)
																			septimo_hijos = GetHijosOfDevice(sexto_hijo)
																			AddElement(septimo_hijos, list_total_dispositivos)
																			if len (septimo_hijos) > 0:
																				for septimo_hijo in septimo_hijos:
																					if ExisteInLista(septimo_hijo, list_elements)==0:
																						print inicio, "│    │    │    │    │    │    │    ├─", GetInforDeviceBySerial(septimo_hijo)
																						octavos_hijos = GetHijosOfDevice(septimo_hijo)
																						AddElement(octavos_hijos, list_total_dispositivos)
																						if len (octavos_hijos) > 0:
																							for octavo_hijo in octavos_hijos:
																								if ExisteInLista(octavo_hijo, list_elements)==0:
																									print inicio, "│    │    │    │    │    │    │    │    ├─", GetInforDeviceBySerial(octavo_hijo)
																									novenos_hijos = GetHijosOfDevice(octavo_hijo)
																									AddElement(novenos_hijos, list_total_dispositivos)
																									if len (novenos_hijos) > 0:
																										for noveno_hijo in novenos_hijos:
																											if ExisteInLista(noveno_hijo, list_elements)==0:
																												print inicio, "│    │    │    │    │    │    │    │    │    ├─", GetInforDeviceBySerial(noveno_hijo)
	return list_total_dispositivos#return list of device insert in tree