#!/usr/bin/env python

# setup.py, script that generate of install modules and create of exect script.
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

from distutils.core import setup

setup(name='DevelopedDevice', version='Version 1',
    description='Gestion de dispositivos en red',
    author='David Medina',
    author_email='dmedina11@alumnos.utalca.cl',
    license='Licencia',
    packages=['ModulosDevice', 'ModulosDevice.ComunicacionDB', 'ModulosDevice.GenerationTree', 'ModulosDevice.Cruds'],
    scripts=['bin/mntools'],
    )