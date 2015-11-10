#!/usr/bin/env python

# Comunication.py, script that manages the communication with the databas,
# as requirement it needs that exist a file with the information of the database,
# which content is :
# host => name of the host
# data base => name of database
# user => user name
# password => keyword
# 
# This file is contained in  ModulosDevice/ComunicacionDB and it's name is conexion.py
# any change in the information of the database make it in that file
# It contains functions for managing communication and functions that allow a simple query
# 
# Copyright (C) 21/10/2015 David Alfredo Medina Ortiz  dmedina11@alumnos.utalca.cl
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

#Modules used
import sys
import psycopg2
import ConfigParser

#Get database information from file
def getDataBaseInfo():

    #instance configparser
    cfg = ConfigParser.ConfigParser()
    cfg.read(["/etc/mn_Tools/db_configuration.cfg"])#read information params in fiel configuration

    #Get the information from the database
    host = cfg.get("connection", "host")
    name = cfg.get("connection", "data_base")
    user = cfg.get("connection", "user")
    password = cfg.get("connection", "password")

    database = {}
    database.update({'host': host})
    database.update({'name': name})
    database.update({'user': user})
    database.update({'password': password})
    return database  

#function that handles communication with the database ...
def BeginComunication():
    database = getDataBaseInfo()
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (database['host'],database['name'],database['user'],database['password'])

    #error handling...
    try:
        db = psycopg2.connect(conn_string)
        return db, db.cursor()#sthe connection is returned to the database and the cursor
    except psycopg2.DatabaseError, e:
        print 'Error %s', e
        sys.exit(1)

#function that manages the query to the database based on the parameters received by argument
def MakeQueryDB (query, database_cursor):

    response = []#list with information from the database ...
    try:
        database_cursor.execute(query)
        for row in database_cursor:
            response.append(row)
        return response
    except psycopg2.DatabaseError, e:
        print 'Error %s', e
        sys.exit(1)