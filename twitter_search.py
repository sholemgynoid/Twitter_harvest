#!/usr/bin/python
# -*- coding: utf-8 -*-

# Accont Developer Gloria Romano
# 
# Consumer Key (API Key)	hymu28pMEQQVTURFz6HNtbeGk
# Consumer Secret (API Secret)	9MBsaoUZzydqul0uHPRbtCqqqDMko05v5VRe9RN07rLI5mOELq
# 
# Access Token	390163215-lWLli6hCtggaAlmqeZruyxlapenQSaMXMQ5Ccu53
# Access Token Secret	Iq3akhGkmICwotk2mJiestoWTx6TqQHpUInxSOHpY6Lfz

import twitter as tw
import json
import cPickle
import nltk
import urllib3
from COSTRUZIONE_DIZIONARIO import *
from IMPORTAZIONE_TWIT_FUNZIONI import *
from TRATTAMENTO_FILE_JSON import *

CONSUMER_KEY = 'hymu28pMEQQVTURFz6HNtbeGk'
CONSUMER_SECRET = '9MBsaoUZzydqul0uHPRbtCqqqDMko05v5VRe9RN07rLI5mOELq'
OAUTH_TOKEN = '390163215-lWLli6hCtggaAlmqeZruyxlapenQSaMXMQ5Ccu53'
OAUTH_TOKEN_SECRET = 'Iq3akhGkmICwotk2mJiestoWTx6TqQHpUInxSOHpY6Lfz'

retry_delay = 2

auth = tw.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = tw.Twitter(
	domain='https://api.twitter.com',
	api_version='1.1',
	auth=auth)


def TWITTER_SEARCH (query_key, since_id, counter, semaforo_scrittura_max_id):
	
	connessione_on = True
	
	file_json = 'Twits_' + query_key + '_' + counter + '.txt'
	file_pickle = "myData_" + query_key + "_" + counter + ".pickle"
	file_frequenze = "FreqDist_" + query_key + "_" + counter + ".txt"

	search_results = []
	testo_out = ""
	
	try:
		search_results = twitter_api.search.tweets(q=query_key,
												since_id=since_id,
												lang='it',
												count=100,
												tweet_mode='extended',
												verify = False)
		tweets = search_results['statuses']
		
		print 'Twit max id str: %s' % search_results['search_metadata']['max_id_str']
		print 'Twit since id str: %s' % search_results['search_metadata']['since_id_str']
		
		print 'Fetched %i tweets so far' % (len(tweets),)
		since_id_new = search_results['search_metadata']['max_id_str']
		
	except (urllib2.URLError, tw.api.TwitterHTTPError) as e:
		print "There is a problem with the URL or with Twitter Server" + str(e) + '\n'
		connessione_on = False
		twit_trovati = 0
	except httplib.BadStatusLine as e:
		print 'PeopleSearch BadStatusLine error: ' + str(e) + '\n'
		connessione_on = False
		twit_trovati = 0
	except socket.error as e:
		print "Couldn't connect to server" + str(e) + '\n'
		connessione_on = False
		twit_trovati = 0
	except urllib2.URLError as e:
		print 'urllib2.URLError' + str(e) + '\n'
		connessione_on = False
		twit_trovati = 0
		
	if semaforo_scrittura_max_id and connessione_on:
		f_since_id = open ('_since_id.txt', 'w')
		f_since_id.write (since_id_new)
		f_since_id.close ()
	
	if connessione_on:
	
		for i in range (40):
	
			print i
	
			try:
				next_results = search_results['search_metadata']['next_results']

			except KeyError:
				break

			kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
		
			kwargs ['since_id'] = since_id
		
			search_results = twitter_api.search.tweets(**kwargs)
			tweets += search_results['statuses']
	
			print 'max id:'
			print search_results['search_metadata']['max_id']
	
			print 'since id:'
			print search_results['search_metadata']['since_id']
	
			print 'Fetched %i tweets so far' % (len(tweets),)
		
			if len(search_results['statuses']) == 0:
				break
		
		twit_trovati = len(tweets)
		
		if twit_trovati > 0:
			testo_out = json.dumps (tweets, sort_keys = True, indent = 1)
		
			f_out = open (file_json, 'wb')
			f_out.write (testo_out)
			f_out.close ()
	
# 			JSON_TO_TEXT (file_json, 'TW_TEXT_' + query_key + '_' + counter + '.txt')
# 			RETWEET_STATS (file_json)
	
# 			tweets = [r['text'] \
# 				for r in tweets]
# 			
# 			words = []
# 			
# 			for t in tweets:
# 	
# 				w = t.split()
# 				lunghezza = len (w)
# 		
# 				for contatore in range (0,lunghezza):
# 					word = PULIZIA_DIZIONARIO (w[contatore].encode('utf-8'))
# 					if word != '':
# 						words.append(word)
# 			
# 			f_out = open(file_pickle, "wb")
# 			cPickle.dump(words, f_out)
# 			f_out.close()
# 	
# 			words = cPickle.load(open(file_pickle))
# 	
# 			freq_dist = nltk.FreqDist (words)
# 	
# 			testo_out = "PRIME CENTO PAROLE" + '\n'
# 	
# 			numero_parole = len(freq_dist.keys())
# 			coda = numero_parole / 3
# 	
# 			PRIME_CENTO_PAROLE = freq_dist.keys()[:101]
# 			ULTIME_CENTO_PAROLE = freq_dist.keys()[-101:]
# 	
# 			for contatore in range (0,100):
# 				try:
# 					testo_out = testo_out + PRIME_CENTO_PAROLE[contatore] + "\n"
# 				except:
# 					testo_out = "Statistiche testuali non rilevate"
# 	
# 			testo_out = testo_out + ('\n' * 2) + "ULTIME CENTO PAROLE" + '\n'
# 	
# 			for contatore in range (0,100):
# 				try:
# 					testo_out = testo_out + ULTIME_CENTO_PAROLE[contatore] + "\n"
# 				except:
# 					testo_out = "Statistiche testuali non rilevate"
# 	
# 			f_out = open(file_frequenze, "wb")
# 			f_out.write (testo_out)
# 			f_out.close ()
	
	return twit_trovati