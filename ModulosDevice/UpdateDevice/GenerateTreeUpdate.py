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

#add element of list to other list...
def AddElement(list_origen, list_destine):

	for element in list_origen:
		list_destine.append(element)

#function that get all elements IPs of file created by GetInformationDevice...
def ListsIPs():

	ListsIPs_elements = []

	command = "awk -F ';' '{print $1}' /home/InformationRedWithFather.csv | uniq -d"
	output = commands.getstatusoutput(command)
	list_element = output[1].split("\n")

	AddElement(list_element, ListsIPs_elements)

	command = "awk -F ';' '{print $1}' /home/InformationRedWithFather.csv | uniq -u"
	output = commands.getstatusoutput(command)
	list_element = output[1].split("\n")
	AddElement(list_element, ListsIPs_elements)

	return ListsIPs_elements
def CreateTreebyIP(IP_address):

	if IP_address in ListsIPs():
		command = "grep \"^%s;\" /home/InformationRedWithFather.csv" % IP_address
		output = commands.getstatusoutput(command)

		List_Information= output[1].split("\n")
		
		#get information of device in csv...
		command = "grep \"^%s;\" /home/InformationRed.csv" % IP_address
		output = commands.getstatusoutput(command)

		line_information = output[1].split("\n")[0].split(";")
		print "├─", line_information
		for element in List_Information:
			list_element = element.split(";")#make a split by ;
			list_new_element = []#with al elements without ip father...
			for i in range (1, len(list_element)):
				list_new_element.append(list_element[i])
			print "│    ├─", list_new_element

			#get information of device in csv...
			command = "grep \"^%s;\" /home/InformationRedWithFather.csv" % line_information[1]
			output = commands.getstatusoutput(command)

			line_information_second = output[1].split("\n")[0].split(";")
			for element_second in line_information_second:
				print "│    │    ├─", list_new_element				

	else:
		print "Not exists IP addres in this moment"
	#print ListsIPs_elements
