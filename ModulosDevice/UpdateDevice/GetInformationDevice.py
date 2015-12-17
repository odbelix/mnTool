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
import ConfigParser

#instance configparser
cfg = ConfigParser.ConfigParser()
cfg.read(["/etc/mn_Tools/db_configuration.cfg"])#read information params in fiel configuration

#Get the information for comunity
comunity = cfg.get("SNMP", "comunity")

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

list_IP_response_SNMP = []
list_IP_already_search = []
list_information_IP_with_father = []

#Get only IP address
def getStringIpFromScan(output):
    result = output.split("\n")
    list_ip = []
    for line in result:
        if len(line) > 50:
            start = line.index("(")
            end = line.index(")")
            list_ip.append(line[start+1:end])
        if len(line) > 25 and len(line) < 50:
            start = line.index("1")
            end = len(line)-1
            list_ip.append(line[start:end+1])
    return list_ip

def HextoStringIp(hexString):
    result = hexString.split("Hex-STRING:")[1]
    result = result[1:-1].split(" ")
    stringIp = ""
    for strData in result:
         stringIp += str(int(strData, 16)) + "."
    return stringIp[:-1]

def OutputToString(outputName):
    result = outputName.split("STRING:")#[1]
    result = result[1][1:-1]
    return result.replace("\"","").lstrip()

def OutputToStringFromInteger(outputName):
    result = outputName.split("INTEGER:")
    result = result[1].replace(" ","")
    return result

def getStringIpFromScan(output):
    result = output.split("\n")
    list_ip = []
    for line in result:
        if len(line) > 50:
            start = line.index("(")
            end = line.index(")")
            list_ip.append(line[start+1:end])
        if len(line) > 25 and len(line) < 50:
            start = line.index("1")
            end = len(line)-1
            list_ip.append(line[start:end+1])
    return list_ip

## Get list of ip address from all switches in private network
def getListOfActiveIp(network):
	print "get element to network %s" %network
	command = "nmap -sP %s | grep '192'" % network
	print command
	output = commands.getstatusoutput(command)
	listIp = getStringIpFromScan(output[1])
	return listIp

#function that convert in string output of SNMP
def OutputToString(outputName):
    result = outputName.split("STRING:")#[1]
    result = result[1][1:-1]
    return result.replace("\"","").lstrip()

#get number serial device by IP
def GetSerialNumeberBySNMP(ip_adress, list_OID):

	command = "snmpwalk -v 1 -c %s %s %s" % (comunity, ip_adress,list_OID['serial'])
	output = commands.getstatusoutput(command)

	return OutputToString(output[1])

#get name of device by IP
def GetNameDeviceBySNMP(ip_adress, list_OID):

	command = "snmpwalk -v 1 -c %s %s %s" % (comunity, ip_adress,list_OID['name'])
	output = commands.getstatusoutput(command)

	return OutputToString(output[1])

#get model of device by IP 
def GetModelDeviceBySNMP(ip_adress, list_OID):
	
	command = "snmpwalk -v 1 -c %s %s %s" % (comunity, ip_adress, list_OID['model'])
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

#get information of interface...
def GetInformationInterface(IP_adress):

	##Getting traffic count for each interface
	command = "snmpwalk -v 1 -c %s %s %s" % (comunity, IP_adress,list_oid_mactraffic["idInterface"])
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
	return listInterfaces

#Getting detail of localInterfaces what has irregular activity
def GetListSummaryInterfaces(IP_adress, listInterfaces):

	listSummaryInterfaces = {}
	for interface in listInterfaces:
		command = "snmpwalk -v 1 -c %s %s %s%s" % (comunity, IP_adress,list_oid_interfaces["idInterface"],"."+interface)
		output = commands.getstatusoutput(command)
		if len(output[1]) is not 0:
			idInterface = OutputToStringFromInteger(output[1])
			listSummaryInterfaces[idInterface] = {}
			listSummaryInterfaces[idInterface]["idInterface"] = interface
				## Diferent name for Interface
                #command = "snmpwalk -v 1 -c public %s %s%s" % (ip_device,"1.3.6.1.2.1.31.1.1.1.1","."+str(OutputToStringFromInteger(output[1])))
                command = "snmpwalk -v 1 -c %s %s %s%s" % (comunity, IP_adress,list_oid_interfaces["localInterface"],"."+str(OutputToStringFromInteger(output[1])))
                output = commands.getstatusoutput(command)
                if len(output[1]) is not 0:
                	## Creating a new list with the summary of traffic mac for each interface
                	listSummaryInterfaces[idInterface]["count"] = listInterfaces[interface]["count"]
                	listSummaryInterfaces[idInterface]["name"] = OutputToString(output[1])
            	else:
            		listSummaryInterfaces.pop(idInterface)
	return listSummaryInterfaces

#function that get traffic of mac for a device...
def GetTrafficDevice(IP_adress, dictOidData):

	List_count = {'enlaces':0}
	List_interfaces = []
	listInterfaces = GetInformationInterface(IP_adress)
	List_count['enlaces'] = len(listInterfaces)
	##Getting detail of localInterfaces what has irregular activity
	listSummaryInterfaces = GetListSummaryInterfaces(IP_adress, listInterfaces)

	for idData in dictOidData:
		key = idData[1:idData[1:].index(".")-len(idData[1:])]
		if key in listSummaryInterfaces.keys():
			if "SEP" in dictOidData[idData]["name"]:
				if listSummaryInterfaces[idData[1:idData[1:].index(".")-len(idData[1:])]]["count"] <= 2:
					listSummaryInterfaces.pop(idData[1:idData[1:].index(".")-len(idData[1:])])
			else:
				listSummaryInterfaces.pop(idData[1:idData[1:].index(".")-len(idData[1:])])

	for interface in listSummaryInterfaces:
		if listSummaryInterfaces[interface]["count"] > 2:
			inter = "%s (%s)" %(listSummaryInterfaces[interface]["name"],listSummaryInterfaces[interface]["count"])
 			List_interfaces.append(inter)
	
	List_count['MAC'] = List_interfaces

	return List_count

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

##Get list of neighbours for one device
def getListOfNeighbours(ip):
    listOidData = []
    dictOidData = {}
    for oid in list_oid_neighbour:
        command = "snmpwalk -v 1 -c %s %s %s" % (comunity, ip,list_oid_neighbour[oid])
        output = commands.getstatusoutput(command)
        outputlist = output[1].split("\n")
        for line in outputlist:
            if any(patter in line for patter in list_patter_keys):
                oidData = line.split(" ")[0].replace(list_oid_neighbour[oid],"")
                if oidData not in listOidData:
                    listOidData.append(oidData)
                    dictOidData[oidData] = {}
                if oid == "address":
                    dictOidData[oidData][oid] = HextoStringIp(line)
                else:
                    dictOidData[oidData][oid] = OutputToString(line)
    result = {'list':listOidData,'dict':dictOidData}
    return result

#Show Information of device
def CreateFileWhitInformation(network):

	list_information = []
	for element in getListOfActiveIp(network):

		information = []

		try:
			information.append(element)
			information.append(GetSerialNumeberBySNMP(element, list_OID))
			information.append(GetNameDeviceBySNMP(element, list_OID))
			information.append(GetModelDeviceBySNMP(element, list_OID))
			list_information.append(information)
			list_IP_response_SNMP.append(element)
			print information
		except:
			print "IP not response ", element
			pass

	name_faile = "InformationRed.csv"
	file_write = open(name_faile, 'a')
	WriteInFile(file_write, list_information)#print element in file csv format...
	file_write.close()

#get statistics of elements (Aps, TIP, RSW, SW)
def GetStatisticsDevice(IP_adress):

	List_count = {'APS':0, 'TIP' :0, 'SW': 0, 'RSW': 0}

	command = "grep \"%s;\" /home/InformationRedWithFather.csv" % IP_adress
	#print command
	output = commands.getstatusoutput(command)
	lines = output[1].split("\n")

	for line in lines:
		list_line = line.split(";")

		if list_line[0] == IP_adress:

			if "SEP" in list_line[3]:
				List_count['TIP']+=1
			if "ap-" in list_line[3]:
				List_count['APS']+=1
			if "sw-" in list_line[3]:
				List_count['SW']+=1
			if "rsw-" in list_line[3]:
				List_count['RSW']+=1
	return List_count

#function that evaluate condition of finish recursive...
def EvaluateFinish(list_element):

	if len(list_element) == 0:
		return 1
	else:
		return 0

#get sib if device by IP address...
def GetNeighbour(IP):
	
	#get neighbour of IP address...
	result = getListOfNeighbours(IP)
	list_new_IP=[]#save a list of ip new device...		
	for element in result["dict"]:
		list_element = []
		list_element.append(IP)
		try:
			#append to list_element => IP father, IP addres, serial, name device, model device
			list_element.append(result["dict"][element]["address"])
			try:
				#print result["dict"][element]["address"]
				list_element.append(GetSerialNumeberBySNMP(result["dict"][element]["address"], list_OID))
			except:
				list_element.append("-")
				pass
			list_element.append(result["dict"][element]["name"])
			list_element.append(result["dict"][element]["model"])
			if result["dict"][element]["address"] not in list_IP_response_SNMP:
				list_IP_response_SNMP.append(result["dict"][element]["address"])
		except:
			pass
		list_new_IP.append(list_element)
		#print list_element
		list_information_IP_with_father.append(list_element)
	return list_new_IP
def main ():
	
	CreateFileWhitInformation("192.168.13.0/24")

	print len (list_IP_response_SNMP)
	for ip in list_IP_response_SNMP:
		GetNeighbour(ip)
		#break

	name_faile = "/home/InformationRedWithFather.csv"
	file_write = open(name_faile, 'w')
	WriteInFile(file_write, list_information_IP_with_father)#print element in file csv format...
	file_write.close()
	
	#Create statidistic for elements, by IP => irregular mac, enlaces, TIP, AP
	list_IP_response_SNMP2 = []
	file_open = open("total_columnas", 'r')
	line = file_open.readline()
	while line:
		line = line.strip("\n")
		list_IP_response_SNMP2.append(line)
		line = file_open.readline()
	
	list_stadisticsTotal = []
	for ip in list_IP_response_SNMP2:
	
		try:
			list_stadistics = []
			list_stadistics.append(ip)
			result = getListOfNeighbours(ip)
			List_count = GetTrafficDevice(ip, result["dict"])
			print List_count
			list_stadistics.append(List_count['enlaces'])
		
			List_count2 = GetStatisticsDevice(ip)
			print List_count2
			list_stadistics.append(List_count2['APS'])
			list_stadistics.append(List_count2['TIP'])
			list_stadistics.append(List_count2['SW'])
			list_stadistics.append(List_count2['RSW'])

			#append irregular macs
			for element in List_count['MAC']:
				list_stadistics.append(element)
					
			list_stadisticsTotal.append(list_stadistics)
			
		except:
			pass

	name_faile = "/home/statidistic.csv"
	file_write = open(name_faile, 'w')
	WriteInFile(file_write, list_stadisticsTotal)#print element in file csv format...
	file_write.close()
	
	return 0

if __name__ == '__main__':
	main()
