#!/usr/bin/env python
########################################################################
# Update device of data base, get device in a network by nmap command and
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
import sys
import os
from ModulosDevice.ComunicacionDB import Comunication
from ModulosDevice.Cruds import Query

#function that read of file and create a list with information
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

#function that allow get name of model by id of model of device
def GetNameModel(id_model):

	query = "select nom_modelo from modelo where id_modelo = %s" % id_model

	database_elements = Comunication.BeginComunication()#init connection
	response = Comunication.MakeQueryDB(query, database_elements[1])#manage query

	return response[0][0]

#function that update ip of device with a NULL value
def UpdateIPDevice(serial, IP):

	query = "update dispositivo set ip_disp = '%s' where serial = '%s'" % (IP,serial)
	Query.UpdateDBWithOutMessage(query)

#function that update name of device with new name and serial of device
def UpdateNameDevice(name_device, serial):

	query = "update dispositivo set nom_disp = '%s' where serial = '%s'" % (name_device, serial)
	Query.UpdateDBWithOutMessage(query)

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
		id_model+=1
		query = "insert into modelo values (%d, %d, %d, '%s')" % (id_model, 0,0, model_device)
		Query.InsertDBWithOutMessage(query)

		query = "update dispositivo set id_modelo = %d where serial = '%s'" % (id_model, serial)
		Query.UpdateDBWithOutMessage(query)


#function that update all device in data base with information get by SNMP
def UpdateDeviceInDataBase():

	file_read = open("information_actual_and_SNMP.csv", 'r')#open output file RecopilaInformatioSNMP.py

	#read file...
	line = file_read.readline()
	while line:

		line = line.strip('\n')
		line_information = line.split(';')
		
		#ask if device response to SNMP...
		if line_information[3] == "si":
		
			#ask if serial exists in data base...
			query = "select * from dispositivo where serial = '%s'" % line_information[0]

			if Query.ExistElementInDB(query) == 0:
				
				#update atributes...
				UpdateIPDevice(line_information[4], line_information[0])
				UpdateNameDevice(line_information[1], line_information[0])
				UpdateModelDevice(line_information[2], line_information[0])
				print line_information
			else:
				#the device not exists in data base... is necesary change element...
				print line_information[0]
				query = "insert into dispositivo values ('%s', %d, '%s', '%s', '%s', %d, %d)" % (line_information[0], 0, line_information[1], '', line_information[4], 0, 0)
				Query.InsertDBWithOutMessage(query)
				UpdateModelDevice(line_information[2], line_information[0])	

		line = file_read.readline()
	
	file_read.close()

#control function...	
def ControlFunction ():

	os.system("python RecopilaInformationSNMP.py")#get information by SNMP and 
	UpdateDeviceInDataBase()
	return 0

def main ():
	ControlFunction()
	return 0

if __name__ == '__main__':
	main()
