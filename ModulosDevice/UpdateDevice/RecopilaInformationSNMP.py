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

list_OID = {'address': '.1.3.6.1.2.1.4.20.1.1',
'serial': '1.3.6.1.4.1.9.5.1.2.19',
'name':'iso.3.6.1.2.1.1.5',
'model': '1.3.6.1.2.1.47.1.1.1.1.13',
'model_alternative': '1.3.6.1.4.1.9.5.1.2.16'}

list_patter_keys = ['Hex-STRING:', 'INTEGER:', 'STRING:']

#function that read of file and create a list with information
def ReadFile(name_file):

	information = []
	file_read = open(name_file, 'r')

	line = file_read.readline()
	while line:
		line = line.strip('\n')
		information.append(line)
		line = file_read.readline()
	return information

#function that write in file whit format csv
def WriteInFile(name_file, list_print):
	#iterate list whit response of data base
	for element in list_print:
		#get information of list element
		for i in range (0, len(element)):
			
			if i == (len(element)-1):
				name_file.write(str(element[i]))
			else:
				var = "%s;"%element[i]
				name_file.write(var)
		name_file.write("\n")
		
#function that convert in string output of SNMP
def OutputToString(outputName):
    result = outputName.split("STRING:")#[1]
    result = result[1][1:-1]
    return result.replace("\"","").lstrip()

#function that allow get all information of one table and create CSV whit its information
def GenerateCSVOfTable(table, query):

	database_elements = Comunication.BeginComunication()#init connection
	response = Comunication.MakeQueryDB(query, database_elements[1])#manage query

	#create file whit information
	name_faile = "%s.csv" % table
	file_write = open(name_faile, 'w')
	WriteInFile(file_write, response)#print element in file csv format...
	file_write.close()
	
#get number serial device by IP
def GetSerialNumeberBySNMP(ip_adress, list_OID):

	command = "snmpwalk -v 1 -c public %s %s" % (ip_adress,list_OID['serial'])
	output = commands.getstatusoutput(command)

	return OutputToString(output[1])

#get name of device by IP
def GetNameDeviceBySNMP(ip_adress, list_OID):

	command = "snmpwalk -v 1 -c public %s %s" % (ip_adress,list_OID['name'])
	output = commands.getstatusoutput(command)

	return OutputToString(output[1])

#get model of device by IP 
def GetModelDeviceBySNMP(ip_adress, list_OID):
	
	command = "snmpwalk -v 1 -c public %s %s" % (ip_adress, list_OID['model'])
	output = commands.getstatusoutput(command)

	line_output = output[1].split('\n')
	
	for element in line_output:#for each element in output snmpwalk, search value not null
		model_parcial = ""#model parcial
		#handler try/except error
		try:
			model_parcial = OutputToString(element)

			if model_parcial[0] == model_parcial[1] and model_parcial[1] == model_parcial[2]:
				model_parcial = ""
			else:
				return model_parcial
		except:
			pass

#function that allow get name of model by id of model of device
def GetNameModel(id_model):

	query = "select nom_modelo from modelo where id_modelo = %s" % id_model

	database_elements = Comunication.BeginComunication()#init connection
	response = Comunication.MakeQueryDB(query, database_elements[1])#manage query

	return response[0][0]

#get new information device by IP address
def GetNewInformationADevice(information_device):

	serial =information_device[0]
	model_device = GetNameModel(information_device[1])
	name_device = information_device[2]
	responde = "-"
	information = []#list whit element compare in data base v/s snmpwalk => serial actual, IP, serial new
	if information_device[4] != '127.0.0.1' and information_device[4] != '-':
	
		try:
			serial = GetSerialNumeberBySNMP(information_device[4], list_OID)
			name_device = GetNameDeviceBySNMP(information_device[4], list_OID)
			model_device= GetModelDeviceBySNMP(information_device[4], list_OID)
			responde = "si"
			#falta obtener el tipo del dispositivo y la marca del dispositivo...
			#falta obtener las puertas de enlace... script mnTool.py
			
		except:
			responde="no"
			pass

	#add elements to list information...
	information.append(serial)#new serial
	information.append(name_device)#new name device
	information.append(model_device)#new model device
	information.append(responde)#add response in case or not.
	information.append(information_device[4])#add IP
	
	return information

#get update information all device whit snmpwalk, create a csv whit information 
def GetNewInformationAllDevice():

	information_DB_SNMP = []#list whit information get of snmp
	device_info = ReadFile("telecomunicaciones.csv")#read csv device and get information...

	for element in device_info:
		
		information_device = element.split(';')#split for get separated element
		information = GetNewInformationADevice(information_device)
		information_DB_SNMP.append(information)
		
	#print information in csv format file
	file_write = open("information_actual_and_SNMP.csv", 'w')
	WriteInFile(file_write, information_DB_SNMP)#print element in file csv format...
	file_write.close()

def OutputToString(outputName):
    result = outputName.split("STRING:")#[1]
    result = result[1][1:-1]
    return result.replace("\"","").lstrip()

def OutputToStringFromInteger(outputName):
    result = outputName.split("INTEGER:")
    result = result[1].replace(" ","")
    return result

def testFunction():

	command = "snmpwalk -v 1 -c public 192.168.13.2 .1.3.6.1.2.1.1.7"
	output = commands.getstatusoutput(command)

	listInterfaces = {}
	for line in output[1].split("\n"):
		if "Error" not in line and any(patter in line for patter in list_patter_keys):
			data = OutputToStringFromInteger(line)
			if str(data) not in listInterfaces.keys():
				listInterfaces[data] = {}
				listInterfaces[data]["count"] = 1
			else:
				listInterfaces[data]["count"] =  listInterfaces[data]["count"] + 1
	print listInterfaces

#control function...	
def ControlFunction ():

	#get back of tables to work
	query = "select * from dispositivo"
	GenerateCSVOfTable("dispositivo", query)#generate csv to table dispositivo
	query = "select * from conecta"
	GenerateCSVOfTable("conecta", query)#generate csv to table 
	query = "select * from dispositivo where nom_disp like '%sw%' or nom_disp like '%rsw%'"#it is the information to query by snmp
	GenerateCSVOfTable("telecomunicaciones", query)
	GetNewInformationAllDevice()
	return 0

def HextoStringIp(hexString):
    result = hexString.split("Hex-STRING:")[1]
    result = result[1:-1].split(" ")
    stringIp = ""
    for strData in result:
         stringIp += str(int(strData, 16)) + "."
    return stringIp[:-1]

def main ():
	#ControlFunction()
	#testFunction()
	print HextoStringIp("iso.3.6.1.2.1.17.1.1.0 = Hex-STRING: 00 19 E8 2B 0B 80")

	return 0

if __name__ == '__main__':
	main()
