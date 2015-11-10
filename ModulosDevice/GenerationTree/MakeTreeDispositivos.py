#!/usr/bin/env python

# MakeTreeDispositivos.py, script that allow manage tree of device in
# base at connection
# 
# Copyright (C) 15/10/2015 David Alfredo Medina Ortiz  dmedina11@alumnos.utalca.cl
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

#Modules use
import sys
import psycopg2

from ModulosDevice.ComunicacionDB import Comunication
from ModulosDevice.Cruds import Query

#function that evaluate if element exists in list
#lista =>
def ExisteInLista(list_serach, element):

	#check existence element in list
	existe =0

	for  element_shows in list_serach:
		if element == element_shows:
			existe=1
			break
	return existe
	
#function that allow create the tree in base at the serials existents in the data base in the table conecta and
#that have match whit atribute serialp
def MakeTreeDevice():

	#create list whit elements shows
	list_elements_shows = []
	
	#generate connection
	database = Comunication.BeginComunication()

	#get list elements fathers
	query = "SELECT serialp from conecta"
	list_serialesp = []#generate list whit information

	serialesp = Comunication.MakeQueryDB (query, database[1])#manage the query

	#storage list of serials
	for element in serialesp:
		list_serialesp.append(element[0])

	#delete elements repeats in list
	list_serialesp = list(set(list_serialesp))
	
	#for each element in list
	for element in list_serialesp:

		#check if exist in elements already show
		if ExisteInLista(list_elements_shows, element) == 0:

			list_parcial = Query.CreateTreeBySerial(element, list_elements_shows, '')#create tree of device
			#append element to list show.
			Query.AddElement(list_parcial, list_elements_shows)

