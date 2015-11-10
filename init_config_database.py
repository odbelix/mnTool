#!/usr/bin/env python

# init_config_database.py, script start configurations of data base, create a file
# whit configuration of data base whit its information:
# 
# "host", "localhost"
# "data_base", "export"
# "user", "david2"
# "password", "12345"
# 
# Copyright (C) David Alfredo Medina Ortiz  dmedina11@alumnos.utalca.cl
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

import ConfigParser  
import os

#function that allow evaluate if exist directory or not
def ExistDirectory():

	exist=0#param to evaluate...
	if os.path.exists("/etc/mn_Tools"):
		os.system("rm -R /etc/mn_Tools")
	if os.path.exists("mn_Tools"):
		os.system("mn_Tools")

#main fuction
def main ():
	cfg = ConfigParser.ConfigParser()#instance of configparser
	cfg.add_section("connection")#add section
	#add element to secction, edit this section if set atributes of connection
	cfg.set("connection", "host", "localhost")
	cfg.set("connection", "data_base", "export")
	cfg.set("connection", "user", "david2")
	cfg.set("connection", "password", "12345")
	ExistDirectory()#evaluate if exists directory
	os.system("mkdir mn_Tools")#create directory
	os.system("cd mn_Tools")#go to new directory
	f = open("db_configuration.cfg", "w")#create file configuration
	cfg.write(f)#write file whit information of configuration
	f.close()#close the file configuration
	os.system("mv db_configuration.cfg mn_Tools")#mv file configuration to directory created
	os.system("mv mn_Tools/ /etc")#move directory to etc directory
	return 0

if __name__ == '__main__':
	main()