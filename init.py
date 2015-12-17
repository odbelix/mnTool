#!/usr/bin/env python

# init.py, script start installation on modules and create configuration file and
# create execute file for all user.
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

import os
<<<<<<< HEAD
import sys

def main():

	os.system("python setup.py install")#exceute setup and install elements in lib and exec in bin
	if len(sys.argv)>1:
		command = "python init_config_database.py %s" % sys.argv[1]
	else:
		command = "python init_config_database.py"
	os.system(command)#create file configuration of connection whit data base.
=======

def main():
	os.system("python setup.py install")#exceute setup and install elements in lib and exec in bin
	os.system("python init_config_database.py")#create file configuration of connection whit data base.
>>>>>>> 02c3ebb0958c363c2794afd4063fb21fbbed3589
	return 0
if __name__ == '__main__':
	main()