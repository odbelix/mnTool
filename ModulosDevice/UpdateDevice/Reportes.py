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

#function that print information in format
def PrintInformationDevice(List_Information, IP):

	try:
		print "Serial Device:\t", List_Information[1]
		print "IP Device:\t", List_Information[0]
		print "Name Device:\t", List_Information[2]
		print "Model Device:\t", List_Information[3]
	except:
		print "%s not exist in registers" % IP
		sys.exit(1)
#function that print information in format
def PrintInformationDeviceReport(List_Information, IP):

	try:
		print "Teleco Conectados:\t", List_Information[1]
		print "TIP:\t", List_Information[3]
		print "APs:\t", List_Information[2]
		print "RSW:\t", List_Information[5]
		print "SW:\t", List_Information[4]

		print "Macs Irregulares: "
		for i in range (6, len(List_Information)):
			print List_Information[i]
	except:
		print "%s not exist in registers" % IP
		sys.exit(1)

#function that get information device by IP => Mac Irregulares, TIP, AP, enlaces
def GetInformationDeviceReport(IP):

	command = "grep \"^%s;\" /home/statidistic.csv" % IP
	output = commands.getstatusoutput(command)

	List_Information = output[1].split("\n")[0].split(";")

	return List_Information


#function that get all information of device by IP => serial, IP, Model, Name
def GetInformationDevice(IP):

	try:
		command = "grep \"^%s;\" /home/InformationRed.csv" % IP
		output = commands.getstatusoutput(command)

		List_Information= output[1].split("\n")[0].split(";")#get information 

		return List_Information
	except:
		print "%s not exist in registers" % IP
		sys.exit(1)

#function that get all information of device by Serial => serial, IP, Model, Name
def GetInformationDeviceSerial(Serial):

	try:
		command = "grep \"%s\" /home/InformationRed.csv" % Serial
		output = commands.getstatusoutput(command)

		List_Information= output[1].split("\n")[0].split(";")#get information 

		return List_Information
	except:
		print "%s not exist in registers" % IP
		sys.exit(1)

#function that get IP addres by serial...
def GetIpBySerialDevice(serial):

	try:
		command = "grep \"%s\" /home/InformationRed.csv" % serial
		output = commands.getstatusoutput(command)

		List_Information= output[1].split("\n")[0].split(";")#get information 

		return List_Information[0]
	except:
		print "%s not exist in registers" % serial
		sys.exit(1)

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

#function that create the csv file with the full report...
def GenerateFullReport():
	date_current = (time.strftime("%d%m%Y"))#get a date of generate report
	#try:
	#read information of file InformationRead.csv
	file_Red = open("/home/InformationRed.csv", "r")

	line = file_Red.readline()
	List_Information_CSV = []#for save information for all csv file

	while line:

		list_information_partial=[]
		#get information and statistics of information
		line = line.strip("\n")
		line_information = line.split(";")
		line_information_statistics =GetInformationDeviceReport(line_information[0])
		#append information of device...
		for element in line_information:
			list_information_partial.append(element)
		try:	
			#append information of statistics device...			
			for i in range (0,5):

				list_information_partial.append(line_information_statistics[i])

			
			#append information of cantidad of irregular macs...
			macs_irregulares = len(line_information_statistics)-6
			list_information_partial.append(macs_irregulares)
			#print list_information_partial
			#append list to list with all elements...
			List_Information_CSV.append(list_information_partial)
		except:
			pass
		line = file_Red.readline()#get a new line of file

	name_file = "Report_%s.csv"%date_current
	file_write = open(name_file, 'w')
	WriteInFile(file_write, List_Information_CSV)#print element in file csv format...
	file_write.close()
	#except:
	#	print "Is not possible create the full report because not exists file csv with information"
