#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Passi di: Matthew A. Russell. “Mining the Social Web”. iBooks. 

#from __future__ import print_function

import twitter
import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine
import json
import io
import pdb
from IMPORTAZIONE_TWIT_FUNZIONI import *
from TRATTAMENTO_FILE_JSON import *

pdb.set_trace()

def harvest_user_timeline (twitter_api, screen_name=None, user_id=None, max_results=1000, since_id=1, semaforo_scrittura_max_id = False):

	assert (screen_name != None) != (user_id != None), "Must have screen_name or user_id, but not both"
	
	print '********** screenname = ' + screen_name
	print '********** max_results = ' + str (max_results)
	print '********** since_id = ' + str (since_id)

	# setting delle keyword per la chiamata alle API di Twitter
	
	kw = {
		'count': max_results,
		#'trim_user': 'true',
		'include-rts': 'true',
		'since_id': since_id
		}
		
# 	'trim_user':
#	When set to either true, t or 1, each tweet returned in a timeline
# 	will include a user object including only the status authors numerical ID.
# 	Omit this parameter to receive the complete user object.

# 	'include-rts':
#	When set to either true, t or 1,the timeline will contain native retweets
# 	(if they exist) in addition to the standard stream of tweets.
# 	The output format of retweeted tweets is identical to the representation
# 	you see in home_timeline.
# 	Note: If you're using the trim_user parameter in conjunction with include_rts,
# 	the retweets will no longer contain a full user object.
		
	if screen_name:
		kw ['screen_name'] = screen_name
	else:
		kw ['user_id'] = user_id
	
	print kw
	
	max_pages = 36
	
	results = []
	
	print twitter_api.statuses.user_timeline
	
	tweets = make_twitter_request (twitter_api.statuses.user_timeline, **kw)
	
	print tweets
	
	if tweets is None:
		print 'no tweets'
		tweets = []
	
	results += tweets
	
	print >> sys.stderr, 'Fetched %i tweets' % len(tweets)
	
	if max_results == kw['count']:
		page_num = max_pages
		
	while page_num < max_pages and len (tweets) > 0 and len (results) < max_results:
		kw ['max_id'] = min ([tweet ['id'] for tweet in tweets]) - 1
	
		tweets = make_twitter_request (twitter_api.statuses.user_timeline, **kw)
		
		results += tweets
		
		print >> sys.stderr, 'Fetched %i tweets' % len(tweets)
		
		page_num += 1
		
	print >> sys.stderr, 'Done fetching tweets'

	if semaforo_scrittura_max_id:
		f_since_id = open ('_since_id.txt', 'w')
		f_since_id.write (str (kw ['max_id']) )
		f_since_id.close ()
	
	return results [:max_results]
	
def make_twitter_request (twitter_api_func, max_errors=10, *args, **kw):

	def handle_twitter_http_error (e, wait_period = 2, sleep_when_rate_limited = True):
		
		if wait_period >3600:
		
			print >> sys.stderr, 'too many retries -> Quitting'
			raise e
			
		if e.e.code == 401:
		
			print >> sys.stderr, 'Encountered 401 Error (Not authorized)'
			return none
		
		elif e.e.code == 404:
		
			print >> sys.stderr, 'Encountered 404 Error (Not found)'
			return None
			
		elif e.e.code == 429:
		
			print >> sys.stderr, 'Encountered 429 Error (Rate limit exceeded)'
			
			if sleep_when_rate_limited:
			
				print >> sys.stderr, 'Retrying in 15 minutes... ZzZ...'
				sys.stderr.flush ()
				time.sleep (60*15+5)
				print >> sys.stderr, 'ZzZ... Awake now and trying again.'
				return 2
			
			else:
			
				raise e
	
	wait_period = 2
	error_count = 0
	
	while True:
	
		print '********** AVVIO RICERCA TWITTER'
		
		try:
			return twitter_api_func (*args, **kw)
		except twitter.api.TwitterHTTPError, e:
			error_count = 0
			wait_period = handle_twitter_http_error (e, wait_period)
			if wait_period is None:
				return
		except URLError, e:
			error_count += 1
			print >> sys.stderr, 'URLError encoutered. Continuing.'
			if error_count > max_errors:
				print >> sys.stderr, 'Too many consecutive errors... bailing out.'
				raise
		except BadStatusLine, e:
			error_count += 1
			print >> sys.stderr, 'BadStatusLine encountered. Continuing.'
			if error_count > max_errors:
				print >> sys.stderr, 'Too many consecutive errors... bailing out.'
				raise
				
def save_json (filename, data):
	
	with io.open ('{0}.json'.format(filename), 'w', encoding = 'utf-8') as f:
	
		f.write (unicode (json.dumps (data, ensure_ascii = False)))
		
def read_json (filename):

	with io.open ('{0}.json'.format(filename), encoding = 'utf-8') as f:
	
		return f.read()	

def TL_SEARCH (query_key, since_id, counter, semaforo_scrittura_max_id):

	CONSUMER_KEY = 'Pamn0ueC69u03fkdycusA'
	CONSUMER_SECRET = 'ItyZn827YfKLZVP4V3wYlnyTa7jeAJX67PJ6k8mgW8'
	OAUTH_TOKEN = '138054290-bOt6Pc5jwbQ35E5naH3HOq1Q8Xq7ubpXUBzJGSDy'
	OAUTH_TOKEN_SECRET = '3Qxa6VpBesPs6PHHvyNulD7ggn49AvmdXbbC3OI'
	
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	
	twitter_api = twitter.Twitter (
		domain='api.twitter.com',
		api_version='1.1',
		auth=auth
		)
	
	tweets = harvest_user_timeline (twitter_api, screen_name = query_key, max_results = 3600, since_id = since_id, semaforo_scrittura_max_id = semaforo_scrittura_max_id)
	
	file_json = query_key + '-' + counter
	file_txt = 'TW_TEXT_' + query_key + '_' + counter + '.txt'
	
	save_json (file_json, tweets)
	
	JSON_TO_TEXT (file_json + '.json', file_txt)
	
	return len (tweets)