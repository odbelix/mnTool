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

#function that create tree with sw and rsw
def CreateTree(IP_addres):

	List_IP_already = []#list with ip 
	List_IP_already.append(IP_addres)
	try:
		#information device
		serial = GetInformationDevice.GetSerialNumeberBySNMP(IP_addres, list_OID)
		name_device = GetInformationDevice.GetNameDeviceBySNMP(IP_addres, list_OID)
		model_device = GetInformationDevice.GetModelDeviceBySNMP(IP_addres, list_OID)
		print "├─ (%s, %s, %s, %s)" % (serial, IP_addres, model_device, name_device)
	
		#traffic
		try:
			result = GetInformationDevice.getListOfNeighbours(IP_addres)
			#remove elements of list where not are sw or rsw
			for elements in result["dict"]:
				if "sw-" in result["dict"][elements]["name"] or "rsw-" in result["dict"][elements]["name"]:
					if result["dict"][elements]["address"] not in List_IP_already:
						print "│    ├─ (%s, %s, %s)" % (result["dict"][elements]["address"], result["dict"][elements]["model"], result["dict"][elements]["name"])
					List_IP_already.append(result["dict"][elements]["address"])

					try:
						#get son of ip addres device...
						result2 = GetInformationDevice.getListOfNeighbours(result["dict"][elements]["address"])
						for elements_son in result2["dict"]:
							if "sw-" in result2["dict"][elements_son]["name"] or "rsw-" in result2["dict"][elements_son]["name"]:
								if result2["dict"][elements_son]["address"] not in List_IP_already:
									print "│    │    ├─ (%s, %s, %s)" % (result2["dict"][elements_son]["address"], result2["dict"][elements_son]["model"], result2["dict"][elements_son]["name"])
								List_IP_already.append(result2["dict"][elements_son]["address"])						
								try:
									result3 = GetInformationDevice.getListOfNeighbours(result2["dict"][elements_son]["address"])
									#get son of ip address device...
									for elements_son2 in result3["dict"]:
										if "sw-" in result3["dict"][elements_son2]["name"] or "rsw-" in result3["dict"][elements_son2]["name"]:
											if result3["dict"][elements_son2]["address"] not in List_IP_already:
												print "│    │    │    ├─ (%s, %s, %s)" % (result3["dict"][elements_son2]["address"], result3["dict"][elements_son2]["model"], result3["dict"][elements_son2]["name"])
											List_IP_already.append(result3["dict"][elements_son2]["address"])
											try:
												result4 = GetInformationDevice.getListOfNeighbours(result3["dict"][elements_son2]["address"])
												#get son of ip address device...
												for elements_son3 in result4["dict"]:
													if "sw-" in result4["dict"][elements_son3]["name"] or "rsw-" in result4["dict"][elements_son3]["name"]:
														if result4["dict"][elements_son3]["address"] not in List_IP_already:
															print "│    │    │    │    ├─ (%s, %s, %s)" % (result4["dict"][elements_son3]["address"], result4["dict"][elements_son3]["model"], result4["dict"][elements_son3]["name"])
														List_IP_already.append(result4["dict"][elements_son3]["address"])
														try:
															result5 = GetInformationDevice.getListOfNeighbours(result4["dict"][elements_son3]["address"])
															#get son of ip address device...
															for elements_son4 in result5["dict"]:
																if "sw-" in result5["dict"][elements_son4]["name"] or "rsw-" in result5["dict"][elements_son4]["name"]:
																	if result5["dict"][elements_son4]["address"] not in List_IP_already:
																		print "│    │    │    │    │    ├─ (%s, %s, %s)" % (result5["dict"][elements_son4]["address"], result5["dict"][elements_son4]["model"], result5["dict"][elements_son4]["name"])
																	List_IP_already.append(result5["dict"][elements_son4]["address"])
																	try:
																		result6 = GetInformationDevice.getListOfNeighbours(result5["dict"][elements_son4]["address"])
																		#get son of ip address device...
																		for elements_son5 in result6["dict"]:
																			if "sw-" in result6["dict"][elements_son5]["name"] or "rsw-" in result6["dict"][elements_son5]["name"]:
																				if result6["dict"][elements_son5]["address"] not in List_IP_already:
																					print "│    │    │    │    │    │    ├─ (%s, %s, %s)" % (result6["dict"][elements_son5]["address"], result6["dict"][elements_son5]["model"], result6["dict"][elements_son5]["name"])
																				List_IP_already.append(result6["dict"][elements_son5]["address"])
																	except:
																		pass

														except:
															pass
											except:
												pass
								except:
									pass
					except:
						pass
		except:
			pass								
		
	except:
		print "IP %s not response SNMP " %IP_addres
		sys.exit(0)


#function that create tree with information of device and TIP and Aps
def CreateTreeFull(IP_addres):

	List_IP_already = []#list with ip 
	List_IP_already.append(IP_addres)
	try:
		#information device
		serial = GetInformationDevice.GetSerialNumeberBySNMP(IP_addres, list_OID)
		name_device = GetInformationDevice.GetNameDeviceBySNMP(IP_addres, list_OID)
		model_device = GetInformationDevice.GetModelDeviceBySNMP(IP_addres, list_OID)
		print "├─ (%s, %s, %s, %s)" % (serial, IP_addres, model_device, name_device)
	
		#traffic
		try:
			result = GetInformationDevice.getListOfNeighbours(IP_addres)
			#remove elements of list where not are sw or rsw
			for elements in result["dict"]:
				if result["dict"][elements]["address"] not in List_IP_already:
					print "│    ├─ (%s, %s, %s)" % (result["dict"][elements]["address"], result["dict"][elements]["model"], result["dict"][elements]["name"])
				if "sw-" in result["dict"][elements]["name"] or "rsw-" in result["dict"][elements]["name"]:
					
					try:				
						#get son of ip addres device...
						result2 = GetInformationDevice.getListOfNeighbours(result["dict"][elements]["address"])
						for elements_son in result2["dict"]:
							if result2["dict"][elements_son]["address"] not in List_IP_already:
								print "│    │    ├─ (%s, %s, %s)" % (result2["dict"][elements_son]["address"], result2["dict"][elements_son]["model"], result2["dict"][elements_son]["name"])
							List_IP_already.append(result2["dict"][elements_son]["address"])	
							if "sw-" in result2["dict"][elements_son]["name"] or "rsw-" in result2["dict"][elements_son]["name"]:

								try:
									result3 = GetInformationDevice.getListOfNeighbours(result2["dict"][elements_son]["address"])
									#get son of ip address device...
									for elements_son2 in result3["dict"]:
										if result3["dict"][elements_son2]["address"] not in List_IP_already:
											print "│    │    │    ├─ (%s, %s, %s)" % (result3["dict"][elements_son2]["address"], result3["dict"][elements_son2]["model"], result3["dict"][elements_son2]["name"])
										List_IP_already.append(result3["dict"][elements_son2]["address"])

										if "sw-" in result3["dict"][elements_son2]["name"] or "rsw-" in result3["dict"][elements_son2]["name"]:
											
											try:
												result4 = GetInformationDevice.getListOfNeighbours(result3["dict"][elements_son2]["address"])
												#get son of ip address device...
												for elements_son3 in result4["dict"]:
													if result4["dict"][elements_son3]["address"] not in List_IP_already:
														print "│    │    │    │    ├─ (%s, %s, %s)" % (result4["dict"][elements_son3]["address"], result4["dict"][elements_son3]["model"], result4["dict"][elements_son3]["name"])
													List_IP_already.append(result4["dict"][elements_son3]["address"])
													if "sw-" in result4["dict"][elements_son3]["name"] or "rsw-" in result4["dict"][elements_son3]["name"]:
														try:
															result5 = GetInformationDevice.getListOfNeighbours(result4["dict"][elements_son3]["address"])
															#get son of ip address device...
															for elements_son4 in result5["dict"]:
																if result5["dict"][elements_son4]["address"] not in List_IP_already:
																	print "│    │    │    │    │    ├─ (%s, %s, %s)" % (result5["dict"][elements_son4]["address"], result5["dict"][elements_son4]["model"], result5["dict"][elements_son4]["name"])
																List_IP_already.append(result5["dict"][elements_son4]["address"])
																if "sw-" in result5["dict"][elements_son4]["name"] or "rsw-" in result5["dict"][elements_son4]["name"]:

																	try:
																		result6 = GetInformationDevice.getListOfNeighbours(result5["dict"][elements_son4]["address"])
																		#get son of ip address device...
																		for elements_son5 in result6["dict"]:
																			if result6["dict"][elements_son5]["address"] not in List_IP_already:
																				print "│    │    │    │    │    │    ├─ (%s, %s, %s)" % (result6["dict"][elements_son5]["address"], result6["dict"][elements_son5]["model"], result6["dict"][elements_son5]["name"])
																			List_IP_already.append(result6["dict"][elements_son5]["address"])
																			#if "sw-" in result6["dict"][elements_son5]["name"] or "rsw-" in result6["dict"][elements_son5]["name"]:
																	except:
																		pass
														except:
															pass
											except:
												pass
								except:
									pass
					except:
						pass
					
		except:
			pass								
		List_IP_already.append(result["dict"][elements]["address"])
	except:
		print "IP %s not response SNMP " %IP_addres
		sys.exit(0)
