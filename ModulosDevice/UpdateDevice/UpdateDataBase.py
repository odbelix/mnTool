#!/usr/bin/env python
########################################################################
# RecopilaInformationSNMP.py of data base, get device in a network by nmap command and
# get information of device whit snmp tool and cisco OID, updateing the 
# information in data base 
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
########################################################################
# David Medina Ortiz <dmedina11@alumnos.utalca.cl>
########################################################################
import commands
import sys
from ModulosDevice.ComunicacionDB import Comunication
from ModulosDevice.Cruds import Query

#function that read a csv file...
def ReadFile(name_file):

	information = []
	file_read = open(name_file, 'r')

	line = file_read.readline()
	while line:
		line = line.strip('\n')
		information.append(line)
		line = file_read.readline()
	file_read.close()
	return information

#function that update ip of device with a NULL value
def UpdateIPDevice(serial, IP):

	query = "update dispositivo set ip_disp = '%s' where serial = '%s'" % (IP,serial)
	Query.UpdateDBWithOutMessage(query)

#function that update name of device with new name and serial of device
def UpdateNameDevice(name_device, serial):

	query = "update dispositivo set nom_disp = '%s' where serial = '%s'" % (name_device, serial)
	Query.UpdateDBWithOutMessage(query)

#function that uptade model of device with a serial of device
def InsertModelDevice(model_device):#Falta el id de la marca y del tipo de dispositivo!!!

	#evaluate if exists the model in data base...
	query = "select * from modelo where nom_modelo = '%s'" % model_device
	if Query.ExistElementInDB(query) != 0:#exists in db...
		id_model=0
		#insert model in data base...
		id_model = Query.GetMaxIDinTable('modelo', 'id_modelo')#falta agregar el tipo de dispositivo y la marca...
		if id_model == None:
			id_model=1	
			
		else:
			id_model+=1
		query = "insert into modelo values (%d, %d, %d, '%s')" % (id_model, 0,0, model_device)
		Query.InsertDBWithOutMessage(query)

#function that allow get name of model by id of model of device
def GetNameModel(id_model):

	query = "select nom_modelo from modelo where id_modelo = %s" % id_model

	database_elements = Comunication.BeginComunication()#init connection
	response = Comunication.MakeQueryDB(query, database_elements[1])#manage query

	return response[0][0]

#function that uptade model of device with a serial of device
def UpdateModelDevice(model_device, serial):#Falta el id de la marca y del tipo de dispositivo!!!

	#evaluate if exists the model in data base...
	query = "select * from modelo where nom_modelo = '%s'" % model_device
	if Query.ExistElementInDB(query) == 0:#exists in db...

		#get the id of model
		query = "select id_modelo from modelo where nom_modelo = '%s'" % model_device
		database_elements = Comunication.BeginComunication()#init connection
		response = Comunication.MakeQueryDB(query, database_elements[1])#manage query

		#update the id of model device...
		query = "update dispositivo set id_modelo = %d where serial = '%s'" % (int(response[0][0]), serial)
		Query.UpdateDBWithOutMessage(query)
	else:#the model device not exist in data base...

		#insert model in data base...
		id_model = Query.GetMaxIDinTable('modelo', 'id_modelo')#falta agregar el tipo de dispositivo y la marca...
		if id_model == None:
			id_model = 0
			query = "insert into modelo values (%d, %d, %d, '%s')" % (id_model, 0,0, model_device)
			Query.InsertDBWithOutMessage(query)

			query = "update dispositivo set id_modelo = %d where serial = '%s'" % (id_model, serial)
			Query.UpdateDBWithOutMessage(query)
		else:
			id_model +=1
			query = "insert into modelo values (%d, %d, %d, '%s')" % (id_model, 0,0, model_device)
			Query.InsertDBWithOutMessage(query)

			query = "update dispositivo set id_modelo = %d where serial = '%s'" % (id_model, serial)
			Query.UpdateDBWithOutMessage(query)

#function that allow get serial of device by IP addres...
def GetSerialDevice(ip_device):

	query = "select serial from dispositivo where ip_disp = '%s'" % ip_device
	print query
	database_elements = Comunication.BeginComunication()#init connection
	response = Comunication.MakeQueryDB(query, database_elements[1])#manage query

	return response[0][0]

#function that insert device in data base...
def InsertDevices(list_element):

	first_element = list_element[0]
	cont=0
	for element in list_element:
		if element == first_element:
			cont+=1
		if cont>1:
			break
		#make split to element
		information_element = element.split(";")
		query = "select * from dispositivo where serial = '%s'" % information_element[1]
		print information_element
		if Query.ExistElementInDB(query) == 1:
			
			query = "insert into dispositivo values ('%s', %d, '%s', '%s', '%s', %d, %d)" % (information_element[1], 0, information_element[2], '', information_element[0], 0, 0)
			Query.InsertDBWithOutMessage(query)
			UpdateModelDevice(information_element[3], information_element[1])
		else:
			#update atributes...
			UpdateIPDevice(information_element[1], information_element[0])
			UpdateNameDevice(information_element[2], information_element[1])
			UpdateModelDevice(information_element[3], information_element[1])

#get information devices son...
def GetInformationDeviceSon(list_information_with_father):

	for element in list_information_with_father:
		list_element = element.split(';')
		if len(list_element) == 5:
			if list_element[2] != '-':
				
				query = "select * from dispositivo where serial = '%s'" % list_element[2]
				
				if Query.ExistElementInDB(query) == 1:
			
					query = "insert into dispositivo values ('%s', %d, '%s', '%s', '%s', %d, %d)" % (list_element[2], 0, list_element[3], '', list_element[1], 0, 0)
					Query.InsertDBWithOutMessage(query)
					UpdateModelDevice(list_element[4], list_element[2])
				else:
					#update atributes...
					UpdateIPDevice(list_element[2], list_element[1])
					UpdateNameDevice(list_element[3], list_element[2])
					UpdateModelDevice(list_element[4], list_element[2])
				
				try:
					#get serial version of device by IP
					serial = GetSerialDevice(list_element[0])
					query = "Insert into conecta values('%s', '%s', %d)" % (serial, list_element[2], 0)
					Query.InsertDBWithOutMessage(query)
				except:
					pass
#main function
def main ():

	list_information_with_father = ReadFile("InformationRedWithFather.csv")
	list_information_device = ReadFile("InformationRed.csv")

	InsertDevices(list_information_device)
	GetInformationDeviceSon(list_information_with_father)

	return 0

if __name__ == '__main__':
	main()