#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import twitter_text
import prettytable

def JSON_TO_TEXT (nome_file_in, nome_file_out):

# -> path del file contenente il tracciato JSON_TO_TEXT
# -> path del file nel quale scrivere il tracciato testo
# Il metodo scrive nel file di output il tracciato testo del record del twit, leggendolo dal file in formato JSON
	
	print 'INIZIO TRATTAMENTO FILE JSON'
	
	text = ''
	text = text.encode('utf-8')
	entities = []
	
	json_data=open (nome_file_in)
	
	try:
		data = json.load(json_data)
	except:
		print nome_file_in
	
	date = [d['created_at'] \
		for d in data]
	
	# Scrivo i dizionari con gli embedding: 'user', con i dati relativi all'utente,
	# 'md', con i dati relativi al tweet
	
	user = [u.setdefault('user', {}) \
		for u in data]
		
# 	md = [meta['metadata'] \
# 		for meta in data]
		
	geoloc = [gl['geo'] \
		for gl in data]
		
	# Raccolgo i dati rilevanti per i tweet
	
	screen_name = [s_n.get('screen_name', 'no name') \
	    for s_n in user]
		
	from_id_user_str = [i_u.get('id_str', '0') \
		for i_u in user]
			
	from_user_name = [u_n.get('name', 'no name') \
		for u_n in user]
			
	user_followers = [u_f.get('followers_count', '0') \
		for u_f in user]	
			
	id = [i['id_str'] \
		for i in data]
			
	geo_loc = [gl['geo'] \
		for gl in data]
				
# 	lang_code = [l_c['iso_language_code'] \
# 		for l_c in md]
		
	profile_image_url = [p_i_u.get('profile_background_image_url', 'no url') \
		for p_i_u in user]
	
	tweets = [r['text'] \
		for r in data]
		
	in_replay_to = [i_r_t['in_reply_to_screen_name'] \
		for i_r_t in data]
		
	in_replay_to_id = [i_r_t_id['in_reply_to_user_id_str'] \
		for i_r_t_id in data]
		
	in_replay_to_sn = [i_r_t_sn['in_reply_to_screen_name'] \
		for i_r_t_sn in data]
		
	for t in tweets:
		entities.append (get_entities (t))
	
	f_out = open (nome_file_out, 'w')
	
	for count in range (0, len(data)):
		f_out.write (date[count] + '\t')
		f_out.write (screen_name[count].encode('utf-8') + '\t')
# 		f_out.write (from_id_user_str[count] + '\t')
		f_out.write (from_user_name[count].encode('utf-8') + '\t')
		f_out.write (id[count] + '\t')
		f_out.write (str(user_followers[count]) + '\t')
# 		f_out.write (profile_image_url[count].encode('utf-8') + '\t')
		f_out.write (tweets[count].encode('utf-8') + '\t')
		
		if in_replay_to[count] is not None:
			f_out.write (in_replay_to[count].encode('utf-8') + '\t')
		else:
			f_out.write ('\t')
			
		if in_replay_to_id[count] is not None:
			f_out.write (in_replay_to_id[count] + '\t')
		else:
			f_out.write ('\t')
			
		if in_replay_to_sn[count] is not None:
			f_out.write (in_replay_to_sn[count].encode('utf-8') + '\t')
		else:
			f_out.write ('\t')
		
# 		if geo_loc[count] is not None:
# 			for coordinate in geo_loc[count]['coordinates']:
# 				f_out.write (str(coordinate) + '\t')
# 		else:
# 			f_out.write ('\t')
			
		if entities[count]['hashtags'][0] is not None:
			for hashtags in entities[count]['hashtags']:
				for hs in hashtags:
					f_out.write (hs.encode('utf-8') + ' ')
		f_out.write ('\t')
			
		if entities[count]['urls'][0] is not None:
			for link in entities[count]['urls']:
				for url in link:
					f_out.write (url + ' ')
		f_out.write ('\t')
			
		if entities[count]['user_mentions'][0] is not None:
			for user_mentions in entities[count]['user_mentions']:
				for user in user_mentions:
					f_out.write (user + ' ')
		f_out.write ('\r')
				
	json_data.close()
	
	# ESTRAZIONE DELLE ENTITIES DAL TESTO DEI TWEET
	
def get_entities (t):

	extractor = twitter_text.Extractor (t)
	
	entities = {}
	
	# Popolo il campo 'user mentions'
	
	entities['user_mentions'] = []
	
	#for um in extractor.extract_mentioned_screen_names():
	entities['user_mentions'].append (extractor.extract_mentioned_screen_names())

	# Popolo il campo 'hashtags'
		
	entities ['hashtags'] = []
	
	#for ht in extractor.extract_hashtags():
	entities['hashtags'].append(extractor.extract_hashtags())
		
	entities['urls'] = []
	
	#for url in extractor.extract_urls():
	entities['urls'].append(extractor.extract_urls())
		
	return entities
	
def RETWEET_STATS (file_in):
	
	json_data=open (file_in)
	
	data = json.load(json_data)

	retweets = [
		(status['retweet_count'],
		status['retweeted_status']['user']['screen_name'],
		status['text'])
		
		for status in data
		
			if status.has_key('retweeted_status')
		]
		
	pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
	[ pt.add_row (row) for row in sorted (retweets, reverse=True) [:5] ]
	pt.max_width ['Text'] = 50
	pt.align= 'l'
	print pt
					
# 	except:
# 		print 'RETWEET_STATS unsuccessful'

	json_data.close()
