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

#create option configuration file
def CreateConfiguration():

	cfg = ConfigParser.ConfigParser()
	cfg.read(["/etc/mn_Tools/db_configuration.cfg"])#read information params in fiel configuration

	print "Configuration Section Data Base?\n<1>Si\n<x>No"
	config_db = raw_input(">> ")

	#evaluate if wish set section connection
	if config_db == "1":
		print "Set configuration Host?\n<1>Si\n<x>No"
		configure_host = raw_input(">>")
		
		#set configuration host
		if configure_host == "1":
			print "Input new host"
			host = raw_input(">> ")
			cfg.set("connection", "host", host)

		print "Set configuration name data base?\n<1>Si\n<x>No"
		configurate_db = raw_input(">> ")

		#set configuration db name
		if configurate_db == "1":
			print "Input new db name"
			db_name = raw_input(">> ")
			cfg.set("connection", "data_base", db_name)

		print "Set configuration user data base?\n<1>Si\n<x>No"
		configuration_user = raw_input(">> ")

		#set configuration user db
		if configuration_user == "1":
			print "Input new name for user db"
			user_db = raw_input(">> ")
			cfg.set("connection", "user", user_db)

		print "Set configuratio password user data base?\n<1>Si\n<x>No"
		configuration_pass = raw_input(">> ")

		#set configuration password
		if configuration_pass == "1":
			print "Input new pass for user"
			pass_user = raw_input(">> ")
			cfg.set("connection", "password", pass_user)

	print "Configuration SNMP option?\n<1>Si\n<x>No"
	config_snmp = raw_input(">> ")

	if config_snmp == "1":

		print "Configurate comunity?\n<1>Si\n<x>No"
		config_comunity = raw_input(">> ")

		#set configuration of comunity
		if config_comunity == "1":
			print "Input new comunity"

			comunity = raw_input(">> ")
			cfg.set("SNMP", "comunity", comunity)

	file_configuration = open("/etc/mn_Tools/db_configuration.cfg", "w")#create file configuration
	cfg.write(file_configuration)


