#!/usr/bin/python
# -*- coding: utf-8 -*-

from Harvest_User_Timeline import *


def RICERCA_TL_CON_CHIAVI ():
		
	f_count = open ('_count.txt')
	contatore = f_count.read()
	f_count.close()
	
	f_since_id = open ('_since_id.txt')
	since_id = f_since_id.read()
	f_since_id.close()
		
	# CHIAVI DI RICERCA
	
	
	L_chiavi_ricerca = [
		'JDMahama'
		]
	
	numero_chiavi = len (L_chiavi_ricerca)
	i = 1
	twit_trovati = 0
	
	for chiave_di_ricerca in L_chiavi_ricerca:
	
		print ('chiave di ricerca: {}'.format(chiave_di_ricerca))
		# try:
		twit_trovati_temp = TL_SEARCH (chiave_di_ricerca, since_id, contatore, i == 1)
		i = i+1
		# except:
		# 	pass
		twit_trovati = twit_trovati + twit_trovati_temp
	
	f_count = open ('_count.txt', 'w')
	f_count.write (str (int(contatore)+1))
	f_count.close ()
	
	return twit_trovati