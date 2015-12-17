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
import time

from ModulosDevice.UpdateDevice import GetInformationDevice

list_OID = {'address': '.1.3.6.1.2.1.4.20.1.1',
'serial': '1.3.6.1.4.1.9.5.1.2.19',
'name':'iso.3.6.1.2.1.1.5',
'model': '1.3.6.1.2.1.47.1.1.1.1.13',
'model_alternative': '1.3.6.1.4.1.9.5.1.2.16'}

list_oid_neighbour = {'address': 'iso.3.6.1.4.1.9.9.23.1.2.1.1.4',
'name': 'iso.3.6.1.4.1.9.9.23.1.2.1.1.6',
'model': 'iso.3.6.1.4.1.9.9.23.1.2.1.1.8'}

list_oid_interfaces = {'localInterface':'iso.3.6.1.2.1.2.2.1.2' , 'idInterface' : 'iso.3.6.1.2.1.17.1.4.1.2' }
list_oid_mactraffic = {'idInterface':'iso.3.6.1.2.1.17.4.3.1.2'}
list_patter_keys = ['Hex-STRING:', 'INTEGER:', 'STRING:']

#Get stattistics of device: APS, TIP, RSW, SW
def GetStatisticsDevice(List_response):

	statistics = {'APS':0, 'TIP' :0, 'SW': 0, 'RSW': 0}#dictionary with counts of elements
	for element in List_response:#count elements
		if ("SEP" in element[3]):
			statistics['TIP']+=1
		if ("ap-" in element[3]):
			statistics['APS']+=1
		if ("sw-" in element[3]):
			statistics['SW']+=1
		if ("rsw-" in element[3]):
			statistics['RSW']+=1
	return statistics

#Get information for generate report all information of device, by IP address
def GenerateReportebyIP(IP_addres):

	#try:
	#information device
	print "Information Device:"
	print "Serial Device: ", GetInformationDevice.GetSerialNumeberBySNMP(IP_addres, list_OID)
	print "IP Device: ", IP_addres
	print "Name Device: ", GetInformationDevice.GetNameDeviceBySNMP(IP_addres, list_OID)
	print "Model Device: ", GetInformationDevice.GetModelDeviceBySNMP(IP_addres, list_OID)
	
	#traffic
	result = GetInformationDevice.getListOfNeighbours(IP_addres)
	List_count = GetInformationDevice.GetTrafficDevice(IP_addres, result["dict"])
	print "Teleco Conectados: ", List_count['enlaces']
	print "Irregular traffic:"
	for element in List_count['MAC']:
		print element

	#statistics neighbour
	print "Statistics Neighbour:"
	statistics = GetStatisticsDevice(GetInformationDevice.GetNeighbour(IP_addres))
	print "Total AP:\t", statistics['APS']
	print "Total TIP:\t", statistics['TIP']
	print "Total RSW:\t", statistics['RSW']
	print "Total SW:\t", statistics['SW']
	
	#except:
	#	print "IP %s not response SNMP " %IP_addres
	#	pass

#print information device if name is AP or SEP...
def PrintNameDevice(List_response, value, option):

	List_append = []
	for element in List_response:
		#print element[3]
		if option == 0:
			
			if "SEP" in element[3]:
				line = "%s/%s" % (element[1], element[3])
				List_append.append(line)
		else:	
			if value[0] == element[3][0] and value[1] == element[3][1]:
				line = "%s/%s" % (element[1], element[3])
				List_append.append(line)
	print List_append

#Get information for generate report full, all information of device, by IP address
def GenerateReporteFullbyIP(IP_addres):

	try:
		#information device
		print "Information Device:"
		print "Serial Device: ", GetInformationDevice.GetSerialNumeberBySNMP(IP_addres, list_OID)
		print "IP Device: ", IP_addres
		print "Name Device: ", GetInformationDevice.GetNameDeviceBySNMP(IP_addres, list_OID)
		print "Model Device: ", GetInformationDevice.GetModelDeviceBySNMP(IP_addres, list_OID)
	
		#statistics neighbour
		print "Statistics Neighbour:"
		List_response = GetInformationDevice.GetNeighbour(IP_addres)
		statistics = GetStatisticsDevice(List_response)
	
		print "Total AP: \t", statistics['APS'], 
		PrintNameDevice(List_response, "ap",1)
		print "Total TIP:\t", statistics['TIP'], 
		PrintNameDevice(List_response, "SEP",0)
		print "Total RSW:\t", statistics['RSW'],
		PrintNameDevice(List_response, "rs",1)
		print "Total SW:\t", statistics['SW'],
		PrintNameDevice(List_response, "sw",1)
	
	#traffic
	#result = GetInformationDevice.getListOfNeighbours(IP_addres)
	#List_count = GetInformationDevice.GetTrafficDevice(IP_addres, result["dict"])
	#print "Teleco Conectados: ", 
	#print "Irregular traffic:"
	#for element in List_count['MAC']:
	#	print element
	except:
	#	print "IP %s not response SNMP " %IP_addres
		pass

#Get irregular mac...
def GenerateReporteErrMac(IP_addres):

	print "Information Device:"
	print "Serial Device: ", GetInformationDevice.GetSerialNumeberBySNMP(IP_addres, list_OID)
	print "IP Device: ", IP_addres
	print "Name Device: ", GetInformationDevice.GetNameDeviceBySNMP(IP_addres, list_OID)
	print "Model Device: ", GetInformationDevice.GetModelDeviceBySNMP(IP_addres, list_OID)

	try:
		#traffic
		result = GetInformationDevice.getListOfNeighbours(IP_addres)
		List_count = GetInformationDevice.GetTrafficDevice(IP_addres, result["dict"])
		print "Teleco Conectados: ", len(result["dict"])
		print "Irregular traffic:"
		for element in List_count['MAC']:
			print element

		if len(List_count['MAC']) >0:
			print "For check the information do:"
			print "telnet "+IP_addres
			print "show mac address interface "+ List_count['MAC'][0]

	except:
		pass
