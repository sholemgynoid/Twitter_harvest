#!/usr/bin/python
# -*- coding: utf-8 -*-

def CHECK_RATE_LIMIT_STATUS ():

	import json as json
	import oauth2
	import httplib2
	import time
	import config
	
	connessione_on = True

	dev_key = config.key_list [config.indice_account_dev]

	# Create your consumer with the proper key/secret.
	consumer = oauth2.Consumer(dev_key ['CONSUMER_KEY'],
							  dev_key ['CONSUMER_SECRET']) 
	# Create your token with the proper key/secret.
	token = oauth2.Token(dev_key ['OAUTH_TOKEN'],
						dev_key ['OAUTH_TOKEN_SECRET'])

	# Request token URL for Twitter.
	rate_limit_url = 'http://api.twitter.com/1.1/application/rate_limit_status.json'

	# Create our client.
	client = oauth2.Client(consumer, token)

	# The OAuth Client request works just like httplib2 for the most part.
	
	try:
		resp, content = client.request(rate_limit_url, "GET")
 		 		
	# Dizionario ritornato esempio:
	# {'x-rate-limit-remaining': '170', 'status': '403', 'content-length': '0',
	# 'set-cookie': 'guest_id=v1%3A138980577900370356; Domain=.twitter.com; Path=/; Expires=Fri, 15-Jan-2016 17:09:39 UTC',
	# 'server': 'tfe', 'x-rate-limit-reset': '1389806529', 'date': 'Wed, 15 Jan 2014 17:09:39 UTC', 'x-rate-limit-limit': '180'}.
	
		data = resp, content
				
		data_dict = data [0]
		
		if 'x-rate-limit-remaining' in data_dict:
			return [data_dict['x-rate-limit-remaining'],
				data_dict['x-rate-limit-reset']]
				
		else:
			return [180, time.time() + 900.0] 


	except httplib2.ServerNotFoundError:
		print ("There is a problem with the Server")
		connessione_on = False
		return [180, time.time() + 900.0]
